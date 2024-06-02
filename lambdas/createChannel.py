import boto3
import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body)
    email = body['email']
    channel_name = body['reason']
    print(email)
    permission = body['permission']

    if permission == 1:
        print("before channel creation")
        channel_arn, stream_key, playback_url,ingest_url  = create_channel(email,channel_name)
        print("after channel creation")
        response_status = send_to_sql_lambda(email, channel_arn, stream_key, playback_url, ingest_url ,permission)
        
        if response_status != 200:
            delete_channel(channel_arn)
    else:
        print("Permission denied for creating IVS channel.")
        send_to_sql_lambda(email, "NoChannel", "NoStreamKey","","", 0)
    response_final = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # This header enables CORS
        }
    }
    return response_final 

def create_channel(email,channel_name):
    ivs_client = boto3.client (
        service_name            = "ivs",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
    try:
       # channel_name = email.split('@')[0]
        response = ivs_client.create_channel(
            name=channel_name,
            latencyMode='LOW',
            type='STANDARD',
            authorized=False,
            recordingConfigurationArn=''
            
        )
        channel_arn = response['channel']['arn']
        stream_key = response['streamKey']['value']
        playback_url = response['channel']['playbackUrl']
        ingest_end = response['channel']['ingestEndpoint']
        
        return channel_arn, stream_key, playback_url,ingest_end 
    except Exception as e:
        print("Failed to create channel:", e)
        raise

def send_to_sql_lambda(email, channel_arn, stream_key,playback_url,ingest_end, permission):
    # = boto3.client('lambda', region_name="us-east-1")
    print("inside the lambda invocation")
    lambda_client= boto3.client(
        service_name            = "lambda",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
    
    payload = {
        "email": email,
        "channel_arn": channel_arn,
        "stream_key": stream_key,
        "permission": permission,
        "playback_url" : playback_url,
        "ingest_end" : ingest_end 
    }
    try:
        response = lambda_client.invoke(
            FunctionName='',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        print(response)
       # response_payload = json.loads(response['Payload'].read())
        response_payload = json.loads(response['Payload'].read().decode("utf-8"))
        print(response_payload)
        return response_payload['statusCode']
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

def delete_channel(channel_arn):
    ivs_client = boto3.client('ivs', region_name="us-east-1")
    try:
        ivs_client.delete_channel(arn=channel_arn)
        print(f"Channel {channel_arn} deleted successfully")
    except Exception as e:
        print(f"Failed to delete channel {channel_arn}: ", e)

