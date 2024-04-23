import os
from psycopg2.extras import NamedTupleCursor
import psycopg2
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')


def get_all_urls(database):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(''' SELECT *
    FROM urls
    ORDER BY urls.id DESC;''')
        urls = curs.fetchall()
        return urls


def get_url_by_name(database, url):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;''',
                     (url, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        url_info = curs.fetchone()
        id_ = url_info.id
        return id_


def get_url_by_id(database, id_):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (id_,))
        url = curs.fetchone()
        return url
