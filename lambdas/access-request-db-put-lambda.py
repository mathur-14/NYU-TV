import json
import mysql.connector


def execute_query(event):
    body = json.loads(event['body'])
    email = body['email']
    reason = body['reason']
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = "INSERT INTO stream_access_requests (account_email, reason) VALUES (%s, %s)"
        cursor.execute(sql, (email, reason))
        connection.commit()
        connection.close
        return 1
    except Exception as e:
        print("Error:", e)
        return 0
        

def lambda_handler(event, context):
    # TODO implement
    print(event)
    res = execute_query(event)
    print("res:",res)
    if res==0:
        return {
            "statusCode":400,
            "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
            },
            "body":str(e),
        }
    else:
        return {
            "statusCode":200,
            "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
            },
            "body":"request put in the DB"
        }

    return res