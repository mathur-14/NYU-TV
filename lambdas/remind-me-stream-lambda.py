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
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None


def insert_to_remind_me(cursor, event_id,streamer_email,event_name,user_email):
    try:
        insert_statement = f"""
            INSERT INTO remind_me (event_id, streamer_email, event_name, user_email)
            VALUES ({event_id}, '{streamer_email}','{event_name}', '{user_email}')
        """
        print(insert_statement)
        cursor.execute(insert_statement)
    except mysql.connector.Error as e:
        print("Error:", e)
        raise

def lambda_handler(event, context):
    body=json.loads(event['body'])
    connection = connect_to_database()

    event_id=body['event_id']
    streamer_email=body['streamer_email']
    event_name=body['event_name']
    user_email=body['user_email']
    if connection is None:
        return {
            'statusCode':500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # This header enables CORS
            },
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        insert_to_remind_me(cursor,event_id ,streamer_email,event_name,user_email)

        return{
            'statusCode':200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # This header enables CORS
            },
            'body':json.dumps({'message':'reminder set'})
        }
        
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred.')
        }
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.commit()
            connection.close()
