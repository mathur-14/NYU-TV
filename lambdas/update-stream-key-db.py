import json
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        return mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def archive_live_event_to_vod(channel_arn,new_stream_key):
    connection = connect_to_database()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Get account_email from channel_arn
        get_email_sql = "SELECT account_email FROM channels WHERE channel_arn = %s"
        cursor.execute(get_email_sql, (channel_arn,))
        email_result = cursor.fetchone()
        if not email_result:
            return False
        account_email = email_result[0]
        # Update the channels table with the new stream key
        update_stream_key_sql = "UPDATE channels SET stream_key = %s WHERE channel_arn = %s"
        cursor.execute(update_stream_key_sql, (new_stream_key, channel_arn))
        
                # Get live event details for the account_email, excluding 'chatroom' and 'playback_url'
        get_live_event_sql = """
        SELECT event_id, event_name, event_date, duration, description, account_email, 
        started_at, is_sports, thumbnail, sport_name, stream_id 
        FROM live_events 
        WHERE account_email = %s
        """
        cursor.execute(get_live_event_sql, (account_email,))
        live_event_details = cursor.fetchone()
        if not live_event_details:
            return False
        
        # Insert into vod_events table
        insert_vod_sql = """
            INSERT INTO vod_events (event_id, event_name, event_date, duration, description, 
            account_email, started_at, is_sports, thumbnail, sports_name, stream_id, recording)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
        """
        cursor.execute(insert_vod_sql, live_event_details)  

        # Delete from live_events
        delete_live_event_sql = "DELETE FROM live_events WHERE account_email = %s"
        cursor.execute(delete_live_event_sql, (account_email,))
        
        connection.commit()
        return True
    except Error as e:
        print("Error processing the request:", e)
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def lambda_handler(event, context):
    channel_arn = event['channel_arn']
    new_stream_key = event['new_stream_key']

    if archive_live_event_to_vod(channel_arn,new_stream_key):
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Live event archived to VOD successfully.'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to archive live event to VOD.'})
        }
