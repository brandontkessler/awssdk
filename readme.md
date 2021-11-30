# AWS SDK

## Redshift

* Import Redshift as a package
* Add credentials
* Query

```python
from awssdk import Redshift
import json

with open('../bcreds.json') as f:
    crd = json.load(f)['redshift']

db = Postgres(crd['database'], 
                crd['ip'], 
                crd['port'], 
                crd['username'], 
                crd['password'])

query = """
    select * from my_table
"""

df = db.query(query)

db.insert_df_to_redshift(df, 'sample_schema')

print(df.head())
```


