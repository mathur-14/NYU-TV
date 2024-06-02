import json
import boto3

def send_emails(subscribers,event_name):
    ses = boto3.client('ses',region_name='us-east-1')
    subject = "Reminder from NYU TV Live"
    body=f"The event by '{event_name}' has gone live! Please join."

    message = {
    'Subject': {
        'Data': subject,
        'Charset': 'UTF-8'
    },
    'Body': {
        'Text': {
            'Data': body,
            'Charset': 'UTF-8'
            }
        }
    }
    ses.send_email(
            Source="y.mathur1498@gmail.com",
            Destination={
                'ToAddresses': ["abc@gmail.com"]
            },
            Message=message
        )
def send_to_sql_lambda(channel_arn,channel_name,stream_id):
    # = boto3.client('lambda', region_name="us-east-1")
    print("inside the lambda invocation")
    lambda_client= boto3.client(
        service_name            = "lambda",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
    
    payload = {
        'channel_arn':channel_arn,
        'channel_name':channel_name,
        'stream_id':stream_id,
    }
    try:
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:211125489044:function:return-event-subscribers-lambda',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        print(response)
       # response_payload = json.loads(response['Payload'].read())
        response_payload = json.loads(response['Payload'].read().decode("utf-8"))
        print(response_payload)
        return response_payload
    except Exception as e:
        print("Error invoking SQL Lambda:", e)
        response_final = {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # This header enables CORS
        }
        
    }
    return response_final 
def lambda_handler(event, context):
    print(event)
    channel_arn = event['resources'][0]
    channel_name = event['detail']['channel_name']
    stream_id = event['detail']['stream_id']
    
    res =  send_to_sql_lambda(channel_arn,channel_name,stream_id)
    subscribers = json.loads(res['subscribers'])
    send_emails(subscribers,channel_name)
    return{
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }