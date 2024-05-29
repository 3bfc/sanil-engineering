import requests
import pandas as pd
df = pd.read_csv('sites.csv')
fields = [
  {
    "type": "PlainText",
    "isRequired": True,
    "displayName": "price"
  },
  {
    "type": "PlainText",
    "isRequired": True,
    "displayName": "price_id"
  },
  {
    "type": "PlainText",
    "isRequired": True,
    "displayName": "frequency"
  }
]

for index, site in df.iterrows():
  url = f"https://api.webflow.com/v2/sites/{site['id']}/collections"
  payload = {
    "displayName": "MS Prices",
    "singularName": "Price"
  }
  headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer b694eb8d4d99c9e34860a5d489146b88530883c22ad4987aedd6f5d1926fb0c1"
  }
  response = requests.post(url, json=payload, headers=headers)
  df.at[index, 'collection_id'] = response.json()['id']
df.to_csv('output_sites.csv', index=False)



payload = {
    "type": "PlainText",
    
    "displayName": "f"
}


fields = [
  {
  "type": "PlainText",
  "displayName": "checked"
  },
  {
    "type": "Number",
    "isRequired": True,
    "displayName": "sort_value"
  }
] 

for index, sites in df.iterrows():
  print(sites['collective'])
  url = f"https://api.webflow.com/v2/collections/{sites['collection_id']}/fields"
  headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer b694eb8d4d99c9e34860a5d489146b88530883c22ad4987aedd6f5d1926fb0c1"
  }
  for field in fields:
    response = requests.post(url, json=field, headers=headers)