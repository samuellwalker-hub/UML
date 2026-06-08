import csv
import mysql.connector

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            user='root',
            password='YourNewPassword123',  
            host='127.0.0.1',               
            port='3306',
            database='Sam'      
        )
    except Exception as error:
        print("Error while connecting to database for Sam", error)
    return connection
    
def load_third_party(connection, file_path_csv):
    cursor = connection.cursor()
    # [Iterate through the CSV file and execute insert statement]
    connection.commit()
    cursor.close()
    return

def query_popular_tickets(connection):
    # Get the most popular ticket in the past month
    sql_statement = """
        SELECT ticket_id, COUNT(*) AS popularity_count
        FROM support_tickets
        WHERE created_at >= NOW() - INTERVAL 1 MONTH
        GROUP BY ticket_id
        ORDER BY popularity_count DESC
        LIMIT 1;
    """
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()
    return records
