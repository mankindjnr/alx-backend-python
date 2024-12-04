import psycopg2
seed = __import__('seed')

def stream_users():
    """
    Streams rows from the 'user_data' table one by one using a generator.
    """
    connection = seed.connect_to_prodev()  # Establish connection to the database

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        
        # Fetch and yield rows one by one using a while loop
        while True:
            row = cursor.fetchone()  # Fetch the next row
            if row is None:
                break  # Exit the loop when no rows are left
            yield row  # Yield the current row
    except Exception as e:
        print(f"Error streaming users: {e}")
    finally:
        cursor.close()
        connection.close()

stream_users()