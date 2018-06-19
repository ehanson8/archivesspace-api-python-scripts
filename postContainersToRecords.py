import json
import requests
import secrets
import csv

targetFile = raw_input('Enter file name: ')
targetRecord = raw_input('Enter record type and id (e.g. \'accessions/2049\'): ')

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

csv = csv.DictReader(open(targetFile))

asRecord = requests.get(baseURL+'/repositories/3/'+targetRecord, headers=headers).json()
print baseURL+'/repositories/3/'+targetRecord
f=open(targetRecord+'asRecordBackup.json', 'w')
json.dump(asRecord, f)
instanceArray = asRecord['instances']

for row in csv:
    uri = row['uri']
    print uri
    top_container = {}
    top_container['ref'] = uri
    sub_container = {}
    sub_container['top_container'] = top_container
    instance = {}
    instance['sub_container'] = sub_container
    instance['instance_type'] = 'mixed_materials'
    instanceArray.append(instance)
asRecord['instances'] = instanceArray
f2=open(targetRecord+'asRecordModified.json', 'w')
json.dump(asRecord, f2)
asRecord = json.dumps(asRecord)
post = requests.post(baseURL+'/repositories/3/'+targetRecord, headers=headers, data=asRecord).json()
print post
