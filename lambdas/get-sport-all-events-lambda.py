import boto3
import json

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Retrieve partition key value from the event
    partition_key_value = json.loads(event['body'])['sport_name']
    
    # Get a reference to the DynamoDB table
    table_name = 'sports'
    table = dynamodb.Table(table_name)
    
    try:
        # Retrieve the item using the partition key
        response = table.get_item(
            Key={
                'sport_name': partition_key_value,
            }
        )
        # Check if the item exists
        if 'Item' in response:
            item = response['Item']
            print("Item read successfully:", item)
        
            return {
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # This header enables CORS
                },
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            print("Item not found")
            return {
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # This header enables CORS
                },
                'statusCode': 404,
                'body': 'Item not found'
            }
    except Exception as e:
        print("Unable to read item:", e)
        return {
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # This header enables CORS
            },
            'statusCode': 500,
            'body': 'Unable to read item'
        }
