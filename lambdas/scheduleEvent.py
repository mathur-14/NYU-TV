import json
import mysql.connector

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

def create_events_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EVENTS (
                event_id INT AUTO_INCREMENT PRIMARY KEY,
                event_name VARCHAR(255) NOT NULL,
                event_date DATETIME NOT NULL,
                duration INT NOT NULL,
                description TEXT,
                account_email VARCHAR(255),
                FOREIGN KEY (account_email) REFERENCES users(account_email)
            )
        """)
    except mysql.connector.Error as e:
        print("Error creating EVENTS table:", e)
        raise
def insert_event(cursor, event_name, event_date, duration, description, email, is_sports, thumbnail, sport_name):
    try:
        sql = """
            INSERT INTO EVENTS (event_name, event_date, duration, description, account_email,is_sports,thumbnail,sport_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (event_name, event_date, duration, description, email, is_sports, thumbnail, sport_name))
    except mysql.connector.Error as e:
        print("Error inserting new event:", e)
        raise

    
def get_event(cursor, event_name,account_email):
    try:
        sql = """
            SELECT * FROM EVENTS where event_name = %s AND account_email= %s;
        """
        cursor.execute(sql, (event_name,account_email))
        res = cursor.fetchall()
        return res[0][0]
    except mysql.connector.Error as e:
        print("Error inserting new event:", e)
        raise
def lambda_handler(event, context):
    connection = None
    try:
        connection = connect_to_database()
        if connection is None:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to connect to the database.')
            }

        cursor = connection.cursor()
        print(event)
        create_events_table(cursor)
        body = json.loads(event['body'])
        event_name = body['event_name']
        event_date = body['event_date']
        duration = body['duration']
        description = body['description']
        email = body['email']
        is_sports = body['is_sports']
        thumbnail = body['thumbnail']
        sport_name = body['sport_name']
        
        insert_event(cursor, event_name, event_date, duration, description, email,is_sports,thumbnail,sport_name)
        

        
        event_id = get_event(cursor,event_name,email)
        connection.commit()
        return {
            'statusCode': 200,
            'body': json.dumps({'event_id':event_id})
        }
        
    except Exception as e:
        if connection is not None:
            connection.rollback()
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred.')
        }
    
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
