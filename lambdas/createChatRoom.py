import boto3
import json

def lambda_handler(event, context):
    ivs_chat_client = boto3.client (
        service_name            = "ivschat",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    print(event)
    event_id = event['queryStringParameters']['event_id']

    try: 
        response = ivs_chat_client.create_room(
            name=event_id,
            maximumMessageRatePerSecond=10,
            maximumMessageLength=500,
        )
        chat_arn = response['arn']
        print(chat_arn)
        payload = {
            'event_id': event_id,
            'chat_arn': chat_arn
        }
        
        lambda_client= boto3.client(
        service_name            = "lambda",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
        invoke_response = lambda_client.invoke(
            FunctionName='',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        print(invoke_response)
        #response_payload = json.loads(response.read().decode("utf-8"))
        #print(invoke_response['statusCode'])
        if invoke_response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
            'statusCode': invoke_response['ResponseMetadata']['HTTPStatusCode'],
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  
        },
            'body': json.dumps({'message': 'Not saved in the table'})
        }
            
    
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  
        },
            'body': json.dumps({
                'message': 'Chat room created successfully',
                'room_id': chat_arn
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  
        },
            'body': json.dumps({'message': 'Failed to create Chat room'})
        }
       
        raise

    