import json
import mysql.connector
def get_row_json(l):
    return {
        'email':l[1],
        'reason':l[2]
    }
def read_records():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM stream_access_requests""")
        result = cursor.fetchall()
        print('result: ', result)
        request_list =[]
        for res in result:
            r=get_row_json(res)
            request_list.append(r)
        connection.commit()
        connection.close()
        
        return request_list

    
    except Exception as e:
        print("Error:", e)
def lambda_handler(event, context):
    result = read_records()
    
    body = {'responseCode':200,'results':result}
    return {
        'statusCode': 200,
        "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
        },

        'body': json.dumps(body)
    }
