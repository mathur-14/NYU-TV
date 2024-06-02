import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

def elastic_delete_all():
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = ''  # the Amazon ES domain, including https://
    index = 'streams'

    url = f"{host}/{index}/_delete_by_query"

    headers = {"Content-Type": "application/json"}

    # Define the query to delete all documents
    delete_query = {
        "query": {
            "match_all": {}
        }
    }

    r = requests.post(url, auth=awsauth, json=delete_query, headers=headers)
    print(r)
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps({"message": "All documents deleted successfully"})
    }

def elastic_put(document):

    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = ''  # the Amazon ES domain, including https://
    index = 'streams'
    type = '_doc'
    url = host + '/' + index + '/' + type

    headers = {"Content-Type": "application/json"}

    r = requests.post(url, auth=awsauth, json=document, headers=headers)
    print(r)
    return {
        "statusCode":200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
                },
        "body": json.dumps({"message": "indexed successfully"})
    }
def lambda_handler(event, context):
    body = json.loads(event['body'])
    doc = {
        'event_id':body['event_id'],
        'description':body['description']
    }
    res = elastic_put(doc)
    return res
    # return elastic_delete_all()
