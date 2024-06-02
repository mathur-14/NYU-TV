import json
import mysql.connector
from datetime import datetime, timedelta

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
def map_scheduled(row):
    event_map = {
        'event_id': row[0],
        'event_name': row[1],
        'event_date': row[2].isoformat(),
        'duration': row[3],
        'description': row[4],
        'account_email': row[5],
        'is_sports': row[6],
        'thumbnail': row[7],
        'sport_name': row[8]
    }
    return event_map

def get_scheduled_events(cursor, event_ids):
    try:
        query = "SELECT * FROM EVENTS WHERE event_id IN ({})".format(','.join(map(str, event_ids)))
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            op =[]
            for e in res:
                op.append(map_scheduled(e))
            return op
        else:
            return []
    except mysql.connector.Error as e:
        print("Error:", e)
        raise
def map_live(row):
    event_map = {
        'event_id': row[0],
        'event_name': row[1],
        'event_date': row[2].isoformat(),
        'duration': row[3],
        'description': row[4],
        'account_email': row[5],
        'started_at': row[6].isoformat(),
        'is_sports': row[7],
        'thumbnail': row[8],
        'sport_name': row[9],
        'chatroom': row[10],
        'playback_url': row[11]
    }
    return event_map

def get_live_events(cursor, event_ids):
    try:
        query = "SELECT * FROM live_events WHERE event_id IN ({})".format(','.join(map(str, event_ids)))
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            op =[]
            for e in res:
                op.append(map_live(e))
            return op
        else:
            return []
    except mysql.connector.Error as e:
        print("Error:", e)
        raise
def map_vod(row):
    event_map = {
        'event_id': row[0],
        'event_name': row[1],
        'event_date': row[2].isoformat(),
        'duration': row[3],
        'description': row[4],
        'account_email': row[5],
        'started_at': row[6].isoformat(),
        'is_sports': row[7],
        'thumbnail': row[8],
        'sports_name': row[9],
        'recording': row[10]
    }
    return event_map

def get_vod_events(cursor, event_ids):
    try:
        query = "SELECT * FROM vod_events WHERE event_id IN ({})".format(','.join(map(str, event_ids)))
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            op =[]
            for e in res:
                op.append(map_vod(e))
            return op
        else:
            return []
    except mysql.connector.Error as e:
        print("Error:", e)
        raise

def lambda_handler(event, context):
    body = json.loads(event['body'])
    event_ids = body['event_ids']
    connection = connect_to_database()
    if connection is None:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to connect to the database.')
        }

    try:
        cursor = connection.cursor()
        vod = get_vod_events(cursor, event_ids)
        live = get_live_events(cursor, event_ids)
        scheduled = get_scheduled_events(cursor, event_ids)
        payload = {
            'live':live,
            'scheduled':scheduled,
            'vod':vod
        }
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(payload)
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
            connection.close()
