import json
import mysql.connector

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

def get_playback_url(cursor, account_email):
    sql = "SELECT playback_url FROM channels WHERE account_email = %s"
    cursor.execute(sql, (account_email,))
    result = cursor.fetchone()
    return result[0] if result else None

def lambda_handler(event, context):
    print(event)
    if 'queryStringParameters' in event and 'account_email' in event['queryStringParameters']:
        account_email = event['queryStringParameters']['account_email']
    else:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Missing account_email query parameter'})
        }

    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        playback_url = get_playback_url(cursor, account_email)
        if playback_url:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  
                },
                'body': json.dumps({'playback_url': playback_url})
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  
                },
                'body': json.dumps('Playback URL not found for the given email.')
            }
    except Exception as e:
        print("Error:", e)
        connection.rollback()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  
            },
            'body': json.dumps('An error occurred while processing your request.')
        }
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
