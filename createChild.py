import os
import sys
from dotenv import load_dotenv
from functions import *
import json

load_dotenv()

filename = str(sys.argv[1])

with open(filename) as data_file:
    data=json.load(data_file)   
oldReq = data['request']

devURL = os.getenv('URL_DEV')
devToken=os.getenv('DEV_AD_TOKEN')
'''print("Please insert ID to create child request:")
reqID = int(input())

response = getReq(devURL, devToken, reqID)
ticketDat=response.json()
oldReq=ticketDat.get("request")'''


input_data={
    "request":{
        "template":{
            "name":"vietpd temp"
        },
        "subject":oldReq.get('subject'),
        "description":oldReq.get('description'),
        "requester":{
            "name":oldReq.get('requester').get('name')
        },
        "udf_fields":oldReq.get('udf_fields')
    }
}
#input_data='%s' % input_data


makeNewReq=newReq(devURL, devToken, {'input_data':str(input_data)})
print(makeNewReq.status_code)
newReq=makeNewReq.json()
if (newReq.get('response_status').get('status_code') == 2000):
    newReqID=newReq.get('request').get('id')
    addRes(devURL, devToken, oldReq.get('id'), f'New request created with ID {newReqID}')
    #linkReq(devURL, devToken, oldReq.get('id'), newReqID)
    print(oldReq.get('id'))
    print(newReqID)
else:
    print(makeNewReq.text)

#addRes=requests.post
#print(makeNewReq.text)
