import json
import boto3

def lambda_handler(event, context):
    account_email = event['account_email']
    labels = event['labels']
    s3_bucket = event['s3_bucket']
    s3_key = event['s3_key']
        
    ses_client = boto3.client (
            service_name            = "ses",
            aws_access_key_id       = "",
            aws_secret_access_key   = "",
            region_name             = "us-east-1",
        ),
    # Send email notification
    email_subject = "URGENT - Video Moderation Alert - NYU LIVE TV"
    email_body = "Your current stream violates our terms and conditions. "
    for violation in violations:
        email_body += f"- {violation}\n"
    email_body += "\nIf these violations are not rectified, we will be forced to end your stream. Please take immediate action to comply with our terms and conditions."
    to_addresses = ["abc@gmail.com"]
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

    

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully')
    }
