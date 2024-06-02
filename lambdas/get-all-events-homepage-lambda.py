import json
import mysql.connector
from datetime import datetime

def create_events_table():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS live_events (
                event_id INT PRIMARY KEY,
                event_name VARCHAR(255) NOT NULL,
                event_date DATETIME NOT NULL,
                duration INT NOT NULL,
                description TEXT,
                account_email VARCHAR(255),
                started_at DATETIME NOT NULL,
                FOREIGN KEY (account_email) REFERENCES users(account_email)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def return_scheduled_event_json(l):
    return{
        'event_id': l[0],
        'event_title': l[1],
        'event_time': l[2].isoformat(),
        'event_duration': l[3],
        'event_description': l[4],
        'event_streamer': l[5],
        'imageUrl':l[7]
    }
def get_all_scheduled_events():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM EVENTS;
        """)
        res = cursor.fetchall()
        print(res)
        op =[]
        for e in res:
            op.append(return_scheduled_event_json(e))
        connection.commit()
        cursor.close()
        connection.close()
        return op
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def return_live_event_json(l):
    return{
        'event_id': l[0],
        'event_title': l[1],
        'event_time': l[2].isoformat(),
        'event_duration': l[3],
        'event_description': l[4],
        'event_streamer': l[5],
        'event_started_at':l[6].isoformat(),
        'imageUrl':l[8],
        'chatroom':l[10],
        'playback_url':l[11]
    }
def get_all_live_events():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM live_events")
        res = cursor.fetchall()
        op =[]
        for e in res:
            print(e)
            op.append(return_live_event_json(e))
        connection.commit()
        cursor.close()
        connection.close()
        return op
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def return_vod_event_json(row):
    return{
        'event_id': row[0],
        'event_title': row[1],
        'event_time': row[2].isoformat(),
        'event_duration': row[3],
        'event_description': row[4],
        'event_streamer': row[5],
        'event_started_at': row[6].isoformat(),
        'imageUrl': row[8],
        'recording': row[10]
    }
def get_all_vod_events():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vod_events")
        res = cursor.fetchall()
        op =[]
        for e in res:
            print(e)
            op.append(return_vod_event_json(e))
        connection.commit()
        cursor.close()
        connection.close()
        return op
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def lambda_handler(event, context):
    # TODO implement
    #create_events_table()
    scheduled = get_all_scheduled_events()
    live = get_all_live_events()
    vod = get_all_vod_events()
    body = {
        'scheduled':scheduled,
        'live':live,
        'vod':vod
    }
    print(body)
    return {
        'statusCode':200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # This header enables CORS
        },
        'body': json.dumps(body)
    }
