import os
import mysql.connector
import csv
import datetime as dt


def get_db_connection(username, password, host, port, database):
    connection = None
    try:
        connection = mysql.connector.connect(user='root',
                                             password='YourNewPassword123',  
                                             host='127.0.0.1',               
                                             port='3306',
                                             database='Sam')                                     
        print('successfully connected.')
        
        # Automatically create the 'sales' table if it doesn't exist
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            ticket_id INT,
            trans_date INT,
            event_id INT,
            event_name VARCHAR(255),
            event_date DATE,
            event_type VARCHAR(100),
            event_city VARCHAR(100),
            customer_id INT,
            price DECIMAL(10,2),
            num_tickets INT
        );
        """
        cursor.execute(create_table_query)
        cursor.close()
        print("Table 'sales' verified/created successfully.")
        
    except Exception as error:
        print(error)
        print("Error while connecting to database for job tracker", error)
    return connection


def format_row(row):
    def f_to_date(date_str='2020-08-01'):
        """ convert date formatted string to date"""
        return dt.datetime.strptime(date_str.strip(), '%Y-%m-%d')

    def f_to_date_int(date_str='2020-08-01'):
        """ convert date string to integer"""
        return int(f_to_date(date_str).strftime("%Y%m%d"))

    new_row = (
        int(row[0]), int(f_to_date_int(row[1])), int(row[2]), row[3], f_to_date(row[4]), 
        row[5], row[6], int(row[7]), float(row[8]), int(row[9])
    )
    return new_row


def extract_from_csv(connection, file_path_csv):
    cursor = connection.cursor()

    with open(file_path_csv) as fh:
        reader = csv.reader(fh)
        
        # Skip the text headers so numeric functions like int() don't crash
        next(reader, None) 
        
        for row_raw in reader:
            if not row_raw:
                continue
            # format this row
            row = format_row(row_raw)

            # insert into database
            insert_stmt = "INSERT INTO sales (ticket_id, trans_date, event_id, event_name, event_date, event_type, event_city, customer_id, price, num_tickets) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            cursor.execute(insert_stmt, values)

        connection.commit()
    cursor.close()


def query_popular_tickets(connection):
    # Get the most popular ticket in the past month
    sql_statement = 'select event_name, sum(num_tickets) as total_tickets from sales group by event_name order by 2 desc limit 2;'
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()
    return records

def print_msg(msg):
    print('---- '+ msg)


if __name__ == "__main__":

    try:
        username = input('Please enter the databse username:')
        password = input('Please enter the databse password:') 
        port = int(input('please enter the port(default=3306):'))
        host = input('Please enter the localhost(default="localhost"):') 
        database = input('Please enter the databse(default=\'ticket_system\'):')
        
        #connect to database
        print_msg('connecting to database at {}, {} '.format(host, port, database, username) )
        connection = get_db_connection(username, password, host, port, database)
        print("")

        print_msg('Data loading process started...')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_filename = os.path.join(script_dir, 'load_third_party.csv')
        extract_from_csv(connection, csv_filename)
        print_msg('Data loaded to database....')
        print("")

        #run query
        records = query_popular_tickets(connection)
        print_msg('Analysys completed.')
        print("Here are the top 2 most popular tickets:")

        #print result
        for record in records:
            print('- {}({})'.format(record[0], record[1]))

    except Exception as e:
        print("\n[CRITICAL ERROR DETECTED]")
        print(f"Error Message: {e}")
        import traceback
        traceback.print_exc()
        print('Process aborted')
