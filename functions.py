import requests

def linkReq(host, token, oldID, newID):
    input_data={
        "link_requests":[{
            "linked_request":{
                "id":newID
            }
        }]
    }
    url = host+"/api/v3/requests/"+str(oldID)+"/link_requests"
    headers = {"authtoken":token}
    with requests.Session() as s:
        return s.post(url, headers, data={"input_data":str(input_data)}, verify=False)


def getReq(host, token, id):
    url = host+"/api/v3/requests/"+str(id)
    headers = {"authtoken":token}
    with requests.Session() as s:
        return s.get(url,headers=headers,verify=False)

def newReq(host, token, data):
    url = host+"/api/v3/requests/"
    headers = {"authtoken":token}
    with requests.Session() as s:
        return s.post (url, headers=headers, data=data, verify=False)

def addRes(host, token, id, content):
    url = host+"/api/v3/requests/"+str(id)+"/resolutions"
    headers = {"authtoken":token}
    input_data = {
        "resolution":{
            "content":content
        }
    }
    with requests.Session() as s:
        return s.post(url, headers=headers, data={"input_data":str(input_data)}, verify=False)