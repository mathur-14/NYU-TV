import json
import mysql.connector
def check_user_stream_access(email):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT * FROM users where account_email = '{email}';
        """)
        res = cursor.fetchone()
        if res:
            return res[1]
        else:
            return 0
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def lambda_handler(event, context):
    # TODO implement
    body = json.loads(event['body'])
    res = check_user_stream_access(body['account_email'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'access':res})
    }
