import os
import sys
from dotenv import load_dotenv
from functions import *
import json

load_dotenv()

'''filename = str(sys.argv[1])

with open(filename) as data_file:
    data=json.load(data_file)   
oldReq = data['request']'''

devURL = os.getenv('URL_DEV')
#devURL="http://localhost:8080"
#devToken=os.getenv('DEV_AD_TOKEN')
devToken=os.getenv('VIETPD_TOKEN')
print("Please insert ID to create child request:")
reqID = int(input())

r = getReq(devURL, devToken, reqID)
ticketDat=r.json()
oldReq=ticketDat.get("request")
newSubject=oldReq.get('subject').replace("Tiếp nhận", "Xử lý")
newDes=oldReq.get('description').replace("Tiếp nhận", "Xử lý")
templateName="vietpd temp"

input_data={
    "request":{
        "template":{
            "name":templateName
        },
        "subject":newSubject,
        "description":newDes,
        "requester":{
            "name":oldReq.get('requester').get('name')
        },
        "udf_fields":oldReq.get('udf_fields')
    }
}


makeNewReq=newReq(devURL, devToken, {'input_data':str(input_data)})
print(makeNewReq.status_code)
newReq=makeNewReq.json()
if (isSuccess(makeNewReq)):
    newReqID=newReq.get('request').get('id')
    addRes(devURL, devToken, oldReq.get('id'), f'New request created with ID {newReqID}')
    linkReq(devURL, devToken, oldReq.get('id'), newReqID)
    print(oldReq.get('id'))
    print(newReqID)
else:
    print(makeNewReq.text)

