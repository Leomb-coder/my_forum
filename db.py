import os

import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )

        print('Connection successful')

        return conn

    except psycopg2.Error as e:
        return {
            'success' : False,
            'message' : e,
        }, 500