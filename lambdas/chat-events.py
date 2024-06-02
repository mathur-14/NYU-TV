import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize the IVS Chat client
    ivs_chat_client = boto3.client (
        service_name            = "ivschat",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )

    # Default response object with CORS headers
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST'
        },
        'body': ''
    }

    # Log the incoming event
    print('chatEventHandler received:', event)

    # Parse the incoming request body
    body = json.loads(event['body'])
    arn = body.get('arn')
    event_attributes = body.get('eventAttributes', {})
    event_name = body.get('eventName')

    # Construct parameters for the sendEvent API
    params = {
        'roomIdentifier': arn,
        'eventName': event_name,
        'attributes': event_attributes
    }

    try:
        ivs_chat_client.send_event(**params)
        print("chatEventHandler > IVSChat.sendEvent  Success")
        # Update response for successful event send
        response['body'] = json.dumps({
            'arn': arn,
            'status': 'success'
        })
    except ClientError as error:
        print('ERROR: chatEventHandler > IVSChat.sendEvent:', error)
        response['statusCode'] = 500
        response['body'] = json.dumps({'message': str(error)})
    except Exception as e:
        print('Unexpected ERROR:', e)
        response['statusCode'] = 500
        response['body'] = json.dumps({'message': str(e)})

    print('Response from: {} statusCode: {} body: {}'.format(event.get('path', 'Unknown path'), response['statusCode'], response['body']))
    return response
