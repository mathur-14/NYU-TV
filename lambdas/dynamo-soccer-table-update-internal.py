import json
import boto3

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    table_name = 'sports'
    item = {
        'sport_name': 'soccer',  # Replace with your primary key attribute name and value
        'events': ['goal', 'foul', 'red card', 'yellow card',
                   'offside', 'throw in', 'corner kick', 'goal-kick', 'injury',
                   'substitution', 'game start', 'game end', 'full time', 'half time', '2nd half started',
                   'additional time', 'misc']
    }
    
    # Get a reference to the DynamoDB table
    table = dynamodb.Table(table_name)
    
    try:
        # Insert the item into DynamoDB
        response = table.put_item(Item=item)
        print("Item inserted successfully:", response)
        return {
            'statusCode': 200,
            'body': json.dumps('Item inserted successfully')
        }
    except Exception as e:
        print("Unable to insert item:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Unable to insert item')
        }
