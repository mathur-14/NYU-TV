import json
import boto3

s3 = boto3.client (
        service_name            = "s3",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
lambda_client = boto3.client (
        service_name            = "lambda",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )

def get_highest_rendition_playlist(bucket_name, prefix_name):
   object_path = "{}/events/recording-started.json".format(prefix_name)
   print(object_path)
   object = s3.get_object(Bucket=bucket_name, Key=object_path)
   print(object)
   body = str(object['Body'].read().decode('utf-8'))
   metadata = json.loads(body)
   media_path = metadata["media"]["hls"]["path"]
   renditions = metadata["media"]["hls"]["renditions"]

   highest_rendition = None
   highest_rendition_size = 0

   for rendition in renditions:
       current_rendition_size = rendition["resolution_height"]
       if (current_rendition_size > highest_rendition_size):
           highest_rendition_size = current_rendition_size
           highest_rendition = rendition

   highest_rendition_playlist = media_path + '/' + highest_rendition['path'] + '/' + highest_rendition['playlist']
   return highest_rendition_playlist


def lambda_handler(event, context):
   prefix_name = event["detail"]["recording_s3_key_prefix"]
   bucket_name = event["detail"]["recording_s3_bucket_name"]
   stream_id = event["detail"]["stream_id"]
   print(stream_id)
   rendition_playlist = get_highest_rendition_playlist(bucket_name, prefix_name)
   print("Highest rendition playlist: {}/{}".format(prefix_name, rendition_playlist))
   cloudfront_domain = ""
   cloudfront_url = f"{cloudfront_domain}/{prefix_name}/{rendition_playlist}"
   print(f"CloudFront URL for playback: {cloudfront_url}")
   #return cloudfront_url

   # Invoke the second Lambda function synchronously
   response = lambda_client.invoke(
        FunctionName='',  
        InvocationType='RequestResponse',  
        Payload=json.dumps({
            'stream_id': stream_id,
            'vod_url': cloudfront_url
        })
    )

    # Parse the response
   response_payload = json.loads(response['Payload'].read().decode('utf-8'))
   status_code = response_payload['statusCode']
    
   if status_code == 200:
        return {
            'statusCode': 200,
            'body': json.dumps({'cloudfront_url': cloudfront_url})
        }
   else:
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred in the second Lambda function.')
        }
