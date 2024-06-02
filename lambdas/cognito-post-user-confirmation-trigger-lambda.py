import json
import mysql.connector
def create_table():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db',
        )
        print(connection)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE users (
        account_email VARCHAR(255) PRIMARY KEY,
        stream_access BOOLEAN)""");
        # cursor.execute("SELECT COUNT(*) FROM users")
        # res = cursor.fetchall()
        # print(res)
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)
    finally:
        if 'connection' in locals():
            connection.close()
def get_all_rows():
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        res = cursor.fetchall()
        print(res)
        cursor.close()
        connection.commit()

    
    except Exception as e:
        print("Error:", e)

def execute_query(email):
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            password='',
            database='nyu_tv_db'
        )
        cursor = connection.cursor()
        sql = "INSERT INTO users (account_email, stream_access) VALUES (%s, %s)"
        cursor.execute(sql, (email,0))
        # cursor.execute("SELECT COUNT(*) FROM users")
        # res = cursor.fetchall()
        # print(res)
        cursor.close()
        connection.commit()

    
    except Exception as e:
        print("Error:", e)
def lambda_handler(event, context):
    # TODO implement
    # print(event)
    get_all_rows()
    if event['triggerSource'] == 'PostConfirmation_ConfirmSignUp':
        email = event['request']['userAttributes']['email']
        execute_query(email)
    else:
        print('event was not a post confirmation. It was a',str(event['triggerSource']),'event')
    return event