import json
import boto3

import boto3

rekognition = boto3.client (
        service_name            = "rekognition",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )

def lambda_handler(event, context):
    try:
        s3_bucket = event["Records"][0]["s3"]["bucket"]["name"]
        s3_key = event["Records"][0]["s3"]["object"]["key"]
        
        # Check if the file is of type jpg, jpeg, or png
        if not s3_key.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f'Skipping non-image file: {s3_key}')
            return {
                'statusCode': 200,
                'body': 'File is not an image, skipping moderation check'
            }
        
        # Assuming channel_name and file_id are parts of the S3 key path
        parts = s3_key.split('/')
        if len(parts) > 3:
            channel_name = parts[2]
            file_id = parts[-1]
        else:
            raise Exception('Invalid S3 key structure')

    except Exception as ex:
        print(ex)
        return {
            'statusCode': 400,
            'body': f'Error parsing S3 trigger: {ex}'
        }

    try:
        response = rekognition.detect_moderation_labels(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_key,
                }
            }
        )
        print(response)
        
        # Check for moderation labels with confidence >= 90%
        violations = [
            label for label in response.get('ModerationLabels', [])
            if label['Confidence'] >= 80.0
        ]
        print(violations)
        
        if violations:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    's3_bucket': s3_bucket,
                    's3_key': s3_key,
                    'channel_arn': channel_name,
                    'violations': violations
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    's3_bucket': s3_bucket,
                    's3_key': s3_key,
                    'channel_arn': channel_name,
                    'violations': []
                })
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error in Rekognition')
        }
