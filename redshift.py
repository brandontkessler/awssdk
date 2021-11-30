import pandas as pd
import psycopg2
import io

class Redshift:
    def __init__(self, db_name, host, port, username, password):
        self.dbname = db_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _connect(self):
        conn = psycopg2.connect(
            dbname = self.dbname, 
            host = self.host, 
            port = self.port, 
            user = self.username, 
            password = self.password
        )
        return conn, conn.cursor()

    def query(self, query):
        conn, cur = self._connect()

        cur.execute(query)

        colnames = [desc[0] for desc in cur.description]
        results = pd.DataFrame(data=cur.fetchall(), columns=colnames)

        conn.close()
    
        return results

    def insert_df_to_redshift(self, df, schema):
        conn, cur = self._connect()

        output = io.StringIO()
        df.to_csv(output, header=False, index=False)
        output.seek(0)
        cur.copy_from(output, schema, null="", sep=',')

        conn.commit()
        conn.close()
        print('successfully inserted data')

        return

if __name__=='__main__':
    # Note use ip address for host
    import json

    with open('../bcreds.json') as f:
        crd = json.load(f)['redshift']
    
    db = Redshift(crd['database'], 
                  crd['ip'], 
                  crd['port'], 
                  crd['username'], 
                  crd['password'])
    
    query = """
        select * from my_table
    """

    df = db.query(query)

    print(df.head())