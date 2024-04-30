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


def add_url_by_name(database, url):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;''',
            (url, datetime.now().date()))
        url_info = curs.fetchone()
        id_ = url_info.id
    conn.commit()
    conn.close()
    return id_


def get_url_by_name(database, url):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT * FROM urls WHERE name = %s", (url,))
        url = curs.fetchone()
        return url


def get_url_by_id(database, id_):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (id_,))
        url = curs.fetchone()
        return url


def add_check(database, id_):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''INSERT INTO url_checks (url_id, created_at, status_code) VALUES (%s, %s, 200) RETURNING id;''',
            (id_, datetime.now().date()))
        check = curs.fetchone()
        id = check.id
    conn.commit()
    conn.close()
    return id


def get_checks(database, id_):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC", (id_,))
        checks = curs.fetchall()
    conn.commit()
    conn.close()
    return checks


def get_latest_check(database, id_):
    conn = psycopg2.connect(database)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY created_at DESC LIMIT 1", (id_,))
        check_date = curs.fetchone()
        conn.commit()
        conn.close()
        return check_date
