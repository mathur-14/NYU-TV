import json
import boto3

def lambda_handler(event, context):
    ivs_client = boto3.client (
        service_name            = "ivs",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    try:
       # channel_name = email.split('@')[0]
        response = ivs_client.create_channel(
            name='trial_recorded_channel',
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