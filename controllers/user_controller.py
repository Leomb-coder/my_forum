from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash
from db import get_connection

def get_all_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT id, username, email, role FROM users''')
        users = cursor.fetchall()

        return users

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_user_by_id(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT id, username, email, role, pfp_url FROM users WHERE id = %s''', (user_id,))
        user = cursor.fetchone()

        return user

    except Exception as e:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_user(username, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id, username, email''', (username, email, password))
        conn.commit()
        user_created = cursor.fetchone()

        return user_created

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM users WHERE id = %s RETURNING id, username, email''', (user_id,))
        conn.commit()
        user = cursor.fetchone()

        return user

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def login_user(email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
        user = cursor.fetchone()

        if user is None:
            return None

        if check_password_hash(user['password'], password):
            user.pop('password', None)
            return user

        return None

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def change_profile_picture(user_id, url):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''UPDATE users SET pfp_url = %s WHERE id = %s RETURNING *''', (url, user_id,))
        conn.commit()
        user = cursor.fetchone()

        if user is None:
            return None

        return user.pop('password', None)

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()