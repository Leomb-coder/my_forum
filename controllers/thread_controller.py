from psycopg2.extras import RealDictCursor
import re
from db import get_connection

def get_forum_threads_count(forum_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT COUNT(id) FROM threads WHERE forum_id = %s''', (forum_id,))
        thread_count = cursor.fetchone()

        return thread_count

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_user_threads_count(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT COUNT(id) FROM threads WHERE user_id = %s''', (user_id,))
        thread_count = cursor.fetchone()

        return thread_count

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_thread_by_id(thread_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM threads WHERE id = %s''', (thread_id,))
        thread = cursor.fetchone()

        return thread

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_threads_by_forum_id(forum_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM threads WHERE forum_id = %s''', (forum_id,))
        threads = cursor.fetchall()

        return threads

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_thread(forum_id, user_id, title, slug, content):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''INSERT INTO threads (forum_id, user_id, title, slug, content) VALUES (%s, %s, %s, %s, %s) RETURNING *''', (
            forum_id, user_id, title, slug, content
        ))
        conn.commit()
        thread_created = cursor.fetchone()

        return thread_created

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def delete_thread(thread_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''DELETE FROM threads WHERE id = %s RETURNING *''', (
            thread_id
        ))
        conn.commit()
        thread_deleted = cursor.fetchone()

        return thread_deleted

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug