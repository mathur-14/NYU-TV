import json
import boto3
from requests_aws4auth import AWS4Auth
import requests

def elastic(query):
    print("elastic module was called")
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = ''
    index = 'streams'
    type = '_doc'

    url = host + '/' + index + '/_search'
    print(url)
    query = {
        "query": {
            "wildcard": {
                "description": "*" + query + "*"
            }
        }
    }


    # ES 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    data = (r.json())
    print(data)
    n = data["hits"]["total"]["value"]
    n = int(n)
    if n == 0:
        print("No results for the query")
        return {
            "statusCode":204, # no results found
            "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
                },
            "body":json.dumps({"results":[]})
        }
    else:
        print(n)
        events = [dict() for x in range(n)]
        for i in range(n):
            event_id = data["hits"]["hits"][i]["_source"]['event_id']
            description = data["hits"]["hits"][i]["_source"]['description']
            events[i]['event_id'] = event_id
            events[i]['description'] = description
        SearchResponse = {
            'statusCode':200,
            'headers':{
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body':json.dumps({'results' : events})
        }
        return SearchResponse
        
def lambda_handler(event, context):
    body = json.loads(event['body'])
    return elastic(body['query'])