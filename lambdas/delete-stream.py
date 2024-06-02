import json
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host='',
        user='',
        password='',
        database='nyu_tv_db'
    )

def delete_stream(event_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(f"""
                DELETE FROM EVENTS where event_id = {event_id};""")
    cursor.execute(f"""
                DELETE FROM live_events where event_id = {event_id};""")
    
    connection.commit()
    cursor.close()
    connection.close()

def lambda_handler(event, context):
    data = json.loads(event['body'])

    delete_stream(data['event_id'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # This header enables CORS
        },
        'body': json.dumps({'message':'deleted stream'})
    }
