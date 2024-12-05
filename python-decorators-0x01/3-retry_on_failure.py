import time
import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection.
    It passes the connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    A decorator that retries a function if it raises an exception.
    :param retries: Number of retry attempts.
    :param delay: Delay between retries in seconds.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)  # Try executing the function
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        time.sleep(delay)  # Wait before retrying
                    else:
                        print("All retries exhausted.")
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database.
    :param conn: Database connection object.
    :return: List of user records.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users after retries: {e}")
