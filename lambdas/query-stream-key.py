import json
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host='',
        user='',
        password='',
        database='nyu_tv_db'
    )

def get_stream_key(email):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(f"""
            SELECT * FROM channels where account_email = '{email}';""")
    res = cursor.fetchall()[0]
    
    connection.commit()
    cursor.close()
    connection.close()
    return res[1],res[2],res[3]

def lambda_handler(event, context):
    data = json.loads(event['body'])

    arn,key,url= get_stream_key(data['email'])

    return {
        'statusCode': 200,
        'body': json.dumps({'channel_arn':arn,'stream_key': key,'ingest_url':url})
    }
