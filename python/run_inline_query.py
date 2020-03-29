import json

import looker_sdk


sdk = looker_sdk.init31()

fields = [
    'hits_eventInfo.eventAction',
    'hits_eventInfo.eventCategory',
]

sort_order = [
    'hits_eventInto.eventCategory asc'
]

body = looker_sdk.models.WriteQuery(
  model= 'google_analytics_block',
  view= 'ga_sessions', # explore is what view means here
  fields= fields,
  
)

response = sdk.run_inline_query('json', body)
data_table = json.loads(response)

print(data_table[0:10])
