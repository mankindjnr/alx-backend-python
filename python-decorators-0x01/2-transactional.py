import sqlite3
import functools

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

def transactional(func):
    """
    A decorator to handle database transactions.
    Commits the transaction if the function executes successfully, rolls back otherwise.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit transaction if no error occurs
            return result
        except Exception as e:
            conn.rollback()  # Rollback transaction on error
            print(f"Transaction failed, rolled back. Error: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates the email of a user in the database.
    :param conn: Database connection object.
    :param user_id: The ID of the user to update.
    :param new_email: The new email address.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully.")
except Exception as e:
    print(f"Failed to update email: {e}")
