import boto3
import json
def get_items_from_dynamodb(event_id):
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')
    
    # Define the table name
    table_name = 'game-events'
    
    # Define the key condition expression
    key_condition_expression = '#pk = :pk_val'
    
    # Define the expression attribute names
    expression_attribute_names = {'#pk': 'event_id'}
    
    # Define the expression attribute values
    expression_attribute_values = {':pk_val': {'S': event_id}}
    
    # Query DynamoDB
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    
    # Extract items from response
    items = response.get('Items', [])
    
    return items

def lambda_handler(event, context):
    # Get partition key from event or any other source
    body = json.loads(event['body'])
    partition_key = str(body['event_id'])
    # Get items from DynamoDB
    items = get_items_from_dynamodb(partition_key)
    print(items)
    if items:
        return {
            'statusCode': 200,
            'headers':{
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps({'items':items})
        }
    return {
        'statusCode': 200,
            'headers':{
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
                },
        'body': json.dumps({"items":[]})
    }
