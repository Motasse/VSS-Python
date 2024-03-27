from __future__ import print_function

import json
import sys
import requests
import smtplib
from smtplib import *
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET

sys.stderr.write("Getting active users from Pulse Secure\n")
url="https://10.0.226.10/api/v1/system/active-users?number=1"
headers={"Authorization":"Basic bjcwdkx0WlE3RVc1U1k2bStmbHE5M28wcncvMEtyQlJOOXZmRkdqbkdXST06"}
subject="[THÔNG BÁO] Đăng nhập đồng thời 2 phiên cho tài khoản "
sender="noc@vss.gov.vn"
cc=["vanhanh@bhxh.gov.vn"]
password="@euM$GT^wGgND3Jo5J"
def send_email(subject, body, sender, to, cc, bcc, password):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=', '.join(to)
    msg['CC']=', '.join(cc)
    receipients=[to]+cc+bcc
    try:
        smtp_server = smtplib.SMTP('smtp.vss.gov.vn', 587) 
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receipients, msg.as_string())
        print("\nMessage sent to "+to)
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        print("Error code: "+error_code+"Message: "+error_message)
def payload(mail):
    root=ET.Element('uid-message')
    ET.SubElement(root,'version').text='1.0'
    ET.SubElement(root, 'type').text='update'
    payload=ET.SubElement(root, 'payload')
    reg=ET.SubElement(payload, 'register-user')
    entry=ET.SubElement(reg, 'entry', user=mail)
    tag=ET.SubElement(entry, 'tag')
    ET.SubElement(tag, 'member').text='NAC_ACTIVE_SS'
    try:
        with open("payload.txt", 'w') as file:
            try:
                ET.ElementTree(root).write("payload.txt")
            except (IOError, OSError):
                print("Error writing to file")
    except (FileNotFoundError, PermissionError, OSError):
        print("Error opening file")
def tagging(pan_ip):
    url='https://10.'+str(pan_ip)+'.244.253/api/?type=user-id&vsys=vsys1'
    headers={'X-PAN-KEY':'LUFRPT13UWdWRmJuSUN6TCswVUE4cUJucEN3anhNc1k9bHAxWHQ4SXhmWW1kcjd1ZnJZT3RpN0NWM3hiZk1uZzYvQ2tvSVkwMkhWV29BdVRPNnI4dEplcFZwMHdGb2IwWg=='}
    files={'file':open('payload.txt')}
    r=requests.post(url, files=files, headers=headers, verify=False)
    print(r.content)
    print(open("payload.txt", "r").read())
pano_dict={'hanoi':1, 'hagiang':2, 'caobang':4, 'backan':6, 'tuyenquang':8, 'laocai':10, 'dienbien':11, 'laichau':12, 'sonla':14, 'yenbai':15, 'hoabinh':17, 'thainguyen':19, 'langson':20, 'quangninh':22, 'bacgiang':24, 'phutho':25, 'vinhphuc':26, 'bacninh':27, 'haiduong':30, 'haiphong':31, 'hungyen':33, 'thaibinh':34, 'hanam':35, 'namdinh':36, 'ninhbinh':37, 'thanhhoa':38, 'nghean':40, 'hatinh':42, 'quangbinh':44, 'quangtri':45, 'thuathienhue':46, 'danang':48, 'quangnam':49, 'quangngai':51, 'binhdinh':52, 'phuyen':54, 'khanhhoa':56, 'ninhthuan':58, 'binhthuan':60, 'kontum':62, 'gialai':64, 'daklak':66, 'daknong':67, 'lamdong':68, 'binhphuoc':70, 'tayninh':72, 'binhduong':74, 'dongnai':75, 'brvt':77, 'hochiminh':79, 'longan':80, 'tiengiang':82, 'bentre':83, 'travinh':84, 'vinhlong':86, 'dongthap':87, 'angiang':89, 'kiengiang':91, 'cantho':92, 'haugiang':93, 'soctrang':94, 'baclieu':95, 'camau':96}
with requests.Session() as r:
    response=r.get(url, headers=headers, verify=False)
    url = "https://10.0.226.10/api/v1/system/active-users?number="+str(response.json()['active-users']['total-matched-record-number'])
    response = r.get(url, headers=headers, verify=False)
jdata=response.json()['active-users']
userdat = jdata['active-user-records']['active-user-record']
data = []
user = []
indexes = []
mem = []
for i in range (0, len(userdat)):
    user.append(userdat[i]['active-user-name'])
for i, v in enumerate(user):
    if user.count(v) > 1 and i not in indexes:
        indexes.append(i)
user.clear()
for i in indexes:
    data.append(userdat[i])
# print(json.dumps(data))
for i in data:
    user.append(i['active-user-name'])
user=list(dict.fromkeys(user))
# for i in user:
#     sub1="@"
#     sub2=".vss"
#     idex1=i.index(sub1)
#     idex2=i.index(sub2)
#     domain=i[idex1+len(sub1):idex2]
#     payload(i)
#     tagging(pano_dict[domain])
#     for j in data:
#         if i==j['active-user-name']:
#             mem.append(j['user-sign-in-time'])
#             mem.append(j['user-roles'])
#     body="Các phiên đăng nhập:\n"+mem[0]+"\t"+mem[1]+"\n"+mem[2]+"\t"+mem[3]
#     send_email(subject+str(i), body, sender, ["dviet.p@gmail.com"], [], [], password)
#     mem.clear()
# if "testvpn@langson.vss.gov.vn" in user:
#     payload("testvpn@langson.vss.gov.vn")
#     tagging(pano_dict["langson"])
sys.stderr.write("Total active users: "+str(jdata['total-returned-record-number']))
sys.stderr.write("\nTotal duplicate users: "+str(len(user)))
