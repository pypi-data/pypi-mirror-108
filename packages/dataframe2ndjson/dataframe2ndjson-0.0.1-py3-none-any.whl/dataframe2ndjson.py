import json
from sys import path
import pandas as pd

def df_to_ndjson(df,path):
    json_df=df.to_json(orient='records')
    data = json.loads(json_df)
    result = [json.dumps(record) for record in data]
    with open(path,'w') as obj:
        for i in result:
            obj.write(i+'\n')
