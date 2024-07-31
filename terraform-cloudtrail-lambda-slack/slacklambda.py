import json, os
from urllib import request, parse
from base64 import b64decode 
from io import BytesIO
import gzip

def lambda_handler(event, context):
    #print (event)   # <--this is the incoming event payload from cloudwatch
    f = b64decode(event["awslogs"]["data"])
    buff = BytesIO(f)
    f = gzip.GzipFile(fileobj=buff)
    alarm = f.read ().decode('utf-8')
    alarm = json.loads(alarm)
    print (alarm)
    for i in range (len(alarm["logEvents"])):
        message = json.loads(alarm["logEvents"][i]["message"])
        #print (message) # <--this is the decoded payload we fetch from the event.
        
        user = message['userIdentity']['arn']
        function = message['resources'][0]['ARN']
        notification = f"User '{user}' performed {message['eventName']} on function '{function}' at {message['eventTime']}" 
        
        #notification = f"User {message['userIdentity']['arn']} performed {message['eventName']} on function {message['requestParameters']['functionName']} at {message['eventTime']}" 
        print (notification)
         
        
        url = os.environ['url']
        headers = {"Content-Type": "application/json"}
        payload = bytes(json.dumps({"text": notification}),encoding='utf-8')
        
        
        req =  request.Request(url, data=payload, headers=headers, method="POST")
        r = request.urlopen(req)
        content = r.read().decode('utf-8')
        print(content)
        #response = requests.request("POST", url, data=payload, headers=headers)
        #print(response.text)