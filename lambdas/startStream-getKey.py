import json
import mysql.connector
from datetime import datetime, timedelta
import boto3
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='nyu-tv-db.c1uwsaqok8kg.us-east-1.rds.amazonaws.com',
            user='admin',
            password='admin1234',
            database='nyu_tv_db'
        )
        connection.autocommit = False  
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None

def get_event_start_time_and_email(cursor, event_id):
    sql = "SELECT event_date, account_email FROM EVENTS WHERE event_id = %s"
    cursor.execute(sql, (event_id,))
    result = cursor.fetchone()
    return result

   
def get_stream_key_and_ingest_url_from_channels(cursor, account_email):
    sql = "SELECT stream_key,ingest_url,playback_url FROM channels WHERE account_email = %s"
    cursor.execute(sql, (account_email,))
    result = cursor.fetchone()
    return result if result else (None, None, None)



def transfer_event_to_live(cursor, event_id, stream_key, account_email, playback_url):

    check_sql = "SELECT 1 FROM live_events WHERE account_email = %s"
    cursor.execute(check_sql, (account_email,))
    if cursor.fetchone():
        return {'error': 'User already has a live event'}

    preview_sql = """
        SELECT event_id, event_name, event_date, duration, description, thumbnail, sport_name, is_sports, account_email
        FROM EVENTS
        WHERE event_id = %s
    """
    cursor.execute(preview_sql, (event_id,))
    result = cursor.fetchone()
    print(result)
    
    now = datetime.now()
    # Insert into live_events
    insert_sql = """
        INSERT INTO live_events (event_id, event_name, event_date, duration, description, thumbnail,sport_name, is_sports, account_email,started_at, playback_url)
        SELECT event_id, event_name, event_date, duration, description, thumbnail,sport_name, is_sports,account_email, %s, %s
        FROM EVENTS
        WHERE event_id = %s
    """
    cursor.execute(insert_sql, (now, playback_url, event_id))
    # Delete from EVENTS
    delete_sql = "DELETE FROM EVENTS WHERE event_id = %s"
    cursor.execute(delete_sql, (event_id,))
    return {'success': 'Event transferred to live'}
    
def lambda_handler(event, context):
    common_headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    print(event)
    if 'queryStringParameters' not in event or 'event_id' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'headers': common_headers,
            'body': json.dumps({'message': 'Missing event_id query parameter'})
        }
    
    event_id = event['queryStringParameters']['event_id']
    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'headers': common_headers,
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        event_details = get_event_start_time_and_email(cursor, event_id)
        if not event_details:
            return {
                'statusCode': 404,
                'headers': common_headers,
                'body': json.dumps('Event not found.')
            }

        event_start_time, account_email = event_details
        if datetime.now() >= event_start_time - timedelta(minutes=15):
            stream_key, ingest_url, playback_url = get_stream_key_and_ingest_url_from_channels(cursor, account_email)
            if stream_key:
                transfer_result = transfer_event_to_live(cursor, event_id, stream_key, account_email, playback_url)
                if 'error' in transfer_result:
                    return {
                        'statusCode': 409,
                        'headers': common_headers,
                        'body': json.dumps({'message': transfer_result['error']})
                    }
                connection.commit()
                
                return {
                    'statusCode': 200,
                    'headers': common_headers,
                    'body': json.dumps({'stream_key': stream_key, 'ingest_url': ingest_url})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': common_headers,
                    'body': json.dumps('Stream key not found for the user.')
                }
        else:
            return {
                'statusCode': 403,
                'headers': common_headers,
                'body': json.dumps('Not within the allowed time window to start streaming.')
            }
    except Exception as e:
        print("Error:", e)
        connection.rollback()
        return {
            'statusCode': 500,
            'headers': common_headers,
            'body': json.dumps('An error occurred.')
        }
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

