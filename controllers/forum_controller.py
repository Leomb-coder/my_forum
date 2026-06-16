from psycopg2.extras import RealDictCursor

from db import get_connection

def get_all_forums():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM forums''')
        forums = cursor.fetchall()

        return forums

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_forum(name, slug, description, icon_url, user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''INSERT INTO forums (name, slug, description, icon_url, created_by) VALUES (%s, %s, %s, %s, %s) RETURNING *''', (
            name, slug, description, icon_url, user_id,
        ))
        conn.commit()
        forum_created = cursor.fetchone()

        return forum_created

    except Exception:
        if 'conn' in locals():
            conn.rollback()
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_forum_by_slug(slug):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM forums WHERE slug = %s''', (slug,))
        forum = cursor.fetchone()

        return forum

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_forum_by_id(forum_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM forums WHERE id = %s''', (forum_id,))
        forum = cursor.fetchone()

        return forum

    except Exception:
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()