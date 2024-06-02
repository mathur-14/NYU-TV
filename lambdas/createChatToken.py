import boto3
import json

def lambda_handler(event, context):
    ivs_chat_client = boto3.client (
        service_name            = "ivschat",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    account_email = event['queryStringParameters']['account_email']  
    room_arn = event['queryStringParameters']['room_arn']           
    is_owner = event['queryStringParameters']['is_owner']            
    
   
    if is_owner:
        capabilities = ['SEND_MESSAGE', 'DISCONNECT_USER', 'DELETE_MESSAGE']
    else:
        capabilities = ['SEND_MESSAGE']

    try:
      
        response = ivs_chat_client.create_chat_token(
            userId= account_email,
            capabilities=capabilities,
            roomIdentifier=room_arn,
            sessionDurationInMinutes=180 
        )
        print(response)
     
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps({
                'token': response['token'],
                'sessionExpirationTime':response['sessionExpirationTime'].isoformat(),
                'tokenExpirationTime':response['tokenExpirationTime'].isoformat()
            })
        }
    except ivs_chat_client.exceptions.ResourceNotFoundException:
      
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps({'message': 'Chat room not found'})
        }
    except ivs_chat_client.exceptions.ValidationException:
      
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps({'message': 'Invalid input parameters'})
        }
    except Exception as e:
        print(e)
     
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps({'message': 'Failed to create Chat token due to an unexpected error'})
        }
