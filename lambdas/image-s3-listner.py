import json
import boto3

rekognition = boto3.client (
        service_name            = "rekognition",
        aws_access_key_id       = "",
        aws_secret_access_key   = "",
        region_name             = "us-east-1",
    )
    
    
def send_email(violations):
        ses_client = boto3.client (
            service_name            = "ses",
            aws_access_key_id       = "",
            aws_secret_access_key   = "",
            region_name             = "us-east-1",
        )
        # Send email notification
        email_subject = "Video Moderation Alert - NYU LIVE TV"
        email_body = "Your current stream violates our terms and conditions. "
        for violation in violations:
            email_body += f"- {violation}\n"
        email_body += "\nIf these violations are not rectified, we will be forced to end your stream. Please take immediate action to comply with our terms and conditions."
        to_addresses = ["madhurimaha2405@gmail.com"]
        print(type(to_addresses)) 
        ses_client.send_email(
            Source="madhurimaha2405@gmail.com",
                    Destination={
                        'ToAddresses':  to_addresses
                    },
                    Message={
                        'Subject': {
                            'Data': email_subject,
                            'Charset': 'UTF-8'
                        },
                        'Body': {
                            'Text': {
                                'Data': email_body,
                                'Charset': 'UTF-8'
                            }
                        }
                    }
                )

def lambda_handler(event, context):
    if event is None or "Records" not in event or len(event["Records"]) == 0:
        return {
            'statusCode': 400,
            'body': 'Invalid trigger'
        }
    
    s3_bucket, s3_key, channel_name, file_id = None, None, None, None
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
        
    # Rekognition Image Moderation
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
            send_email(violations)
            print(f'Moderation labels with confidence >= 90% for {s3_key}:')
            for label in violations:
                print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")
        else:
            print(f'No moderation labels with confidence >= 90% found for {s3_key}')
        # Detect general labels
        label_response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_key,
                }
            },
            MaxLabels=10
        )
        image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}}
        print(image)
        
        # Print general labels
        print(f'General labels for {s3_key}:')
        for label in label_response.get('Labels', []):
            print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")
        
        

    
    except Exception as ex:
        print(ex)
        return {
            'statusCode': 500,
            'body': f'Error calling Rekognition: {ex}'
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            's3_bucket': s3_bucket,
            's3_key': s3_key,
            'channel_name': channel_name,
            'file_id': file_id
        })
    }
