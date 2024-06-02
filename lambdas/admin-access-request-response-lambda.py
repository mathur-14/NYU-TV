import json
import mysql.connector
import boto3

def read_users():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )

        cursor = connection.cursor()
        
        # Reading users
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        res = cursor.fetchall()
        print("result: ", res)
        
        # Reading channels
        sql = "SELECT * FROM channels"
        cursor.execute(sql)
        res = cursor.fetchall()
        print("result: ", res)

        connection.commit()
        connection.close()

    except Exception as e:
        print("Error:", e)

def update_records(event):
    print(event)
    email = event['email']
    permission = event['permission']
    channel_arn = event['channel_arn']
    stream_key = event['stream_key']
    playback_url = event['playback_url']
    ingest_end = event['ingest_end']
    
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )

        cursor = connection.cursor()
        connection.start_transaction()

        if(permission == 0):
            sql = "DELETE FROM stream_access_requests WHERE account_email = %s"
            cursor.execute(sql, (email,))
        if(permission == 1):
            sql = "DELETE FROM stream_access_requests WHERE account_email = %s"
            cursor.execute(sql, (email,))
            sql = "UPDATE users SET stream_access = 1 WHERE account_email = %s"
            cursor.execute(sql, (email,))
            
            if channel_arn and stream_key:
                sql = "INSERT INTO channels (account_email, channel_arn, stream_key,playback_url,ingest_url) VALUES (%s, %s, %s,%s,%s)"
                cursor.execute(sql, (email, channel_arn, stream_key,playback_url,ingest_end))

        connection.commit()
        connection.close()

    except Exception as e:
        connection.rollback()
        print("Error:", e)

def lambda_handler(event, context):
    update_records(event)
    # read_users()
    return {
        'statusCode': 200,
        'body': json.dumps('Updated the tables!')
    }
