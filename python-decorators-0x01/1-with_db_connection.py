import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection.
    It passes the connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open database connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the function
        finally:
            conn.close()  # Ensure the connection is closed
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by their ID from the database.
    :param conn: Database connection object.
    :param user_id: The ID of the user to fetch.
    :return: User record as a tuple or None if not found.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)