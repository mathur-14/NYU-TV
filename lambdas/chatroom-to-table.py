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

def update_live_events_with_chat_arn(cursor, event_id, chat_arn):
    sql = """
        UPDATE live_events
        SET chatroom = %s
        WHERE event_id = %s
    """
    cursor.execute(sql, (chat_arn, event_id))

def lambda_handler(event, context):
    #body = json.loads(event['body'])
   # print(event)
    event_id = event['event_id']
    chat_arn = event['chat_arn']

    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        update_live_events_with_chat_arn(cursor, event_id, chat_arn)
        connection.commit()
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Chat ARN saved successfully'})
        }
    except Exception as e:
        print("Error:", e)
        connection.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred during the database update.')
        }
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

