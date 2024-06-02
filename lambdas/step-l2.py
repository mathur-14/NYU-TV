import json
import mysql.connector
import os

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        connection.autocommit = False  
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None

def get_account_email_by_channel_arn(cursor, channel_arn):
    cursor.execute(f"SELECT account_email FROM channels WHERE channel_arn = '{channel_arn}';")
    result = cursor.fetchone()
    return result[0] if result else None

def lambda_handler(event, context):
    channel_arn = event['channel_arn']

    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        account_email = get_account_email_by_channel_arn(cursor, channel_arn)
        if not account_email:
            raise Exception(f'Account email not found for channel ARN: {channel_arn}')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'account_email': account_email,
                'labels': event['labels'],
                's3_bucket': event['s3_bucket'],
                's3_key': event['s3_key']
            })
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error fetching account email: {e}')
        }
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
