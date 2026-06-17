from db import get_connection
from psycopg2.extras import RealDictCursor

def create_reply(thread_id, user_id, content):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''INSERT INTO replies (thread_id, user_id, content) VALUES (%s, %s, %s) RETURNING thread_id''', (
            thread_id,
            user_id,
            content,
        ))
        conn.commit()
        reply = cursor.fetchone()

        return reply

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_replies_by_thread_id(thread_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM replies WHERE thread_id = %s''', (thread_id,))
        replies = cursor.fetchall()

        return replies

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_replies_count_by_user_id(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT COUNT(id) FROM replies WHERE user_id = %s''', (user_id,))
        replies = cursor.fetchone()

        return replies

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_replies_count_by_forum(forum_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('''
            SELECT COUNT(r.id) AS count FROM replies r JOIN threads t ON r.thread_id = t.id WHERE t.forum_id = %s
        ''', (forum_id,))
        replies = cursor.fetchone()

        return replies

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()