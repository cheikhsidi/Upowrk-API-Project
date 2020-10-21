# Illustrates an API call to Datafiniti's Product Database for hotels.
import requests
# import urllib.parse
import json
import pandas as pd
from pandas import json_normalize 
import config

# Set your API parameters here.
data = pd.read_excel('File Summary for  CM Datafiniti.xlsx', dtype=str).head(20)
d = data.to_dict('records')
zips  = ['06902', '06854', '06877', '067706', '06482', '10562', '10994', '10954', '10605', '12601', '07017', '07024', '07065', '07601', '07030']
responses =[]
# for ad in d[:2]:
def datafinityFilter(z):
    API_token = config.API_token
    format = 'JSON'
    # q = 'AND (propertyType:"Single Family Dwelling" OR propertyType:"Residential" OR propertyType:"House" OR  propertyType:"Multi-Family Dwelling")'
    # query = f'address:"{ad}" AND city:"{ct}" AND postalCode:"{str(zip)}"'
    # print(query)
    # num_records = 10
    # download = False
    # price = f'(prices.amountMin300000 AND prices.amountMax:12000000)',
    p =  {"amountMax": 12000000 ,
    "amountMin": 300000}
   
    q = f'(propertyType:"Single Family Dwelling" OR propertyType:"Residential" OR propertyType:"House" OR  propertyType:"Multi-Family Dwelling") AND prices.amountMin:>300000 AND  prices.amountMax:<12000000 AND postalCode:{z}'
    request_headers = {
        'Authorization': 'Bearer ' + API_token,
        'Content-Type': 'application/json',
    }
    request_data = {
        'query': q,
        'format': format,
        # 'num_records': num_records,
        # 'download': download
    }

    # Make the API call.
    r = requests.post('https://api.datafiniti.co/v4/properties/search',json=request_data,headers=request_headers);

    # Do something with the response.
    if r.status_code == 200:
        print(r.content)
        res = json.loads(r.content.decode('utf-8'))
        responses.append(res)
        
    else:
        print('Request failed')


for z in zips[:4]:
    # ad = sam['ownr_st']
    # ct = sam['ownr_city']
    # zi = sam['site_zip']
    # if len(zi) < 5:
    #     zi = '0' + str(zi)
    datafinityFilter(z)
df = json_normalize(responses, 'records')
df.to_excel('test1.xlsx', index=False)