seed = __import__('seed')

def stream_users(connection):
    """
    stream rows from an sql database
    """
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data;")
    row = cursor.fetchone()

    while row:
        yield row
        row = cursor.fetchone()

    cursor.close()
    connection.close()

def main():
    connection = seed.connect_db()
    if connection:
        seed.create_database(connection)
        connection.close()
        print(f"connection successful")

        connection = seed.connect_to_prodev()

        if connection:
            return stream_users(connection)

if __name__ == "__main__":
    main()