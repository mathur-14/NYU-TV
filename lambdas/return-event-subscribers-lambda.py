import json
import mysql.connector
from datetime import datetime, timedelta

def get_streamer_email(channel_arn):

    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = f"SELECT * FROM channels WHERE channel_arn = '{channel_arn}'"
        cursor.execute(sql)
        
        res = cursor.fetchall()[0][0]
        print('fetched streamer_email:',res)
        connection.commit()
        connection.close
        return res
    except Exception as e:
        print("Error:", e)
   
def get_event_id(email):

    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = f"SELECT * FROM live_events WHERE account_email = '{email}'"
        cursor.execute(sql)
        res = cursor.fetchall()[0][0]
        print('fetched event id:',res)
        connection.commit()
        connection.close
        return res
    except Exception as e:
        print("Error:", e)     
def return_event_id(row):
    return row[3]
def get_event_subscribers(event_id):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = f"SELECT * FROM remind_me WHERE event_id = {event_id}"
        cursor.execute(sql)
        res = cursor.fetchall()
        op=[]
        for row in res:
            op.append(return_event_id(row))
        print('fetched subscribers:',op)
        connection.commit()
        connection.close
        return op
    except Exception as e:
        print("Error:", e)     
def update_stream_id(stream_id,event_id):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = f"""UPDATE live_events SET stream_id = '{stream_id}' WHERE event_id = {event_id}"""
        cursor.execute(sql)
        connection.commit()
        connection.close
    except Exception as e:
        print("Error:", e)     

def lambda_handler(event, context):
    channel_arn = event['channel_arn']
    channel_name = event['channel_name']
    stream_id = event['stream_id']
    print("arguements:",channel_arn,channel_name,stream_id)
    # sql
    streamer_email = get_streamer_email(channel_arn)
    event_id = get_event_id(streamer_email)
    subscribers = get_event_subscribers(event_id)
    update_stream_id(stream_id,event_id)
    body = {
        "subscribers":subscribers
    }
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }