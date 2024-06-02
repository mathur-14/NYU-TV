import json
import boto3

def lambda_handler(event, context):

    ivs_client = boto3.client (
        service_name            = "ivs",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )

    channel_arn = event['resources'][0]


    try:
        keys_response = ivs_client.list_stream_keys(channelArn=channel_arn)
        stream_keys = keys_response['streamKeys']
        #ivs_client.delete_stream_key(arn=stream_key['arn'])
        for key in stream_keys:
            ivs_client.delete_stream_key(arn=key['arn'])
        

        new_key_response = ivs_client.create_stream_key(channelArn=channel_arn)
        new_stream_key = new_key_response['streamKey']['value']

        print(f"New stream key created: {new_stream_key}")
        # Prepare to invoke the second Lambda to update the DB
        lambda_client= boto3.client(
        service_name            = "lambda",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
        payload = {
            "channel_arn": channel_arn,
            "new_stream_key": new_stream_key
        }
    
        response = lambda_client.invoke(
            FunctionName='',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        # Check response from the second Lambda
        response_payload = json.loads(response['Payload'].read().decode("utf-8"))
        if 'errorMessage' in response_payload:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to update database', 'details': response_payload})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Stream key reset successfully',
                'new_stream_key': new_stream_key
            })
        }
    except Exception as e:
        print(f"Error handling stream keys for {channel_arn}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to reset stream key',
                'error': str(e)
            })
        }
