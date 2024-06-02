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

def update_vod_events_with_url(cursor, stream_id, vod_url):
    print(stream_id)
    print(vod_url)
    
    #cursor.execute(f"""
    #SELECT * FROM vod_events WHERE stream_id ='{stream_id}';""")
    cursor.execute(f"""
    SELECT * FROM vod_events;""")
    result = cursor.fetchall()
    print('result for all vod events: ', result)
    
    cursor.execute(f"""
    SELECT * FROM vod_events WHERE stream_id ='{stream_id}' ;""")
    result = cursor.fetchall()
    print('result for this vod', result)
    
    sql = f"""
        UPDATE vod_events
        SET recording = '{vod_url}'
        WHERE stream_id = '{stream_id}';
    """
    print(sql)
    cursor.execute(sql)
    
    cursor.execute(f"""
    SELECT * FROM vod_events WHERE event_id=83 ;""")
    result = cursor.fetchall()
    print('result: ', result)
    
    cursor.execute(f"""
    SELECT * FROM vod_events WHERE stream_id ='{stream_id}' ;""")
    result = cursor.fetchall()
    print('result: ', result)
    
def update_vod_events_with_url_try_2(cursor, stream_id, vod_url):
    try:
        print(f"Stream ID: {stream_id}")
        print(f"VOD URL: {vod_url}")
        
        cursor.execute(f"""
        SELECT event_id 
        FROM vod_events 
        WHERE stream_id = %s;""", (stream_id,))
        result = cursor.fetchone()
        
        if result is None:
            print(f"No event found with stream_id: {stream_id}")
            return None
        
        event_id = result[0]
        print(f"Event ID: {event_id}")

        # Step 2: Update the recording column for the event with the given stream_id
        cursor.execute(f"""
        UPDATE vod_events
        SET recording = %s
        WHERE event_id = %s;""", (vod_url, event_id))
        
        # Step 3: Fetch the updated record to confirm the update
        cursor.execute(f"""
        SELECT * 
        FROM vod_events 
        WHERE stream_id = %s;""", (stream_id,))
        updated_result = cursor.fetchall()
        print(f"Updated result: {updated_result}")
        
        return updated_result
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    
    
    

def lambda_handler(event, context):
    stream_id = event['stream_id']
    vod_url = event['vod_url']
    print(stream_id)

    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        update_vod_events_with_url_try_2(cursor, stream_id, vod_url)
        connection.commit()
        print("done")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'VOD URL saved successfully'})
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
