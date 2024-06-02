import json
import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    body=json.loads(event['body'])
    table_name = 'game-events'
    
    item = {
        'event_id':body['event_id'],
        'timestamp':body['timestamp'],
        'sport_name': body['sport_name'],
        'account_email':body['account_email'],
        'event': body['event']
    }
    
    # Get a reference to the DynamoDB table
    table = dynamodb.Table(table_name)
    ivs = boto3.client('ivs')
    try:
        # Insert the item into DynamoDB
        response = table.put_item(Item=item)
        print("Item inserted successfully:", response)
        response = ivs.put_metadata(
        channelArn=body['channel_arn'],
        metadata= body['event']['score']
        )
        print("score updated through ivs metadata")
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # This header enables CORS
            },
            'body': json.dumps('Item inserted successfully')
        }
    except Exception as e:
        print("Unable to insert item:", e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # This header enables CORS
            },
            'body': json.dumps('Unable to insert item')
        }
