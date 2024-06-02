import json
import mysql.connector


def return_live_event_json(l):
    return{
        'event_id': l[0],
        'event_title': l[1],
        'event_time': l[2].isoformat(),
        'event_duration': l[3],
        'event_description': l[4],
        'event_streamer': l[5],
        'started_at':l[6].isoformat(),
        'playback_url':l[11],
        'is_sports':l[7],
        'sport_name':l[9],
        'imageUrl':l[8],
        'chatroom':l[10]
    }
def get_all_scheduled_events(email):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT * FROM live_events where account_email = '{email}';
        """)
        res = cursor.fetchall()
        print(res)
        op =[]
        for e in res:
            op.append(return_live_event_json(e))
        connection.commit()
        cursor.close()
        connection.close()
        return op
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['account_email']

    res = get_all_scheduled_events(email)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # This header enables CORS
        },
        'body': json.dumps({'results': res})
    }
