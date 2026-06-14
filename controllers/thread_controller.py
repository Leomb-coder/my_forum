from psycopg2.extras import RealDictCursor
import re
from db import get_connection

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

def create_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug