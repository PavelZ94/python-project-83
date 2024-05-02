import os
from psycopg2.extras import NamedTupleCursor
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


def connection():
    return psycopg2.connect(DATABASE_URL)


def get_all_urls():
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls ORDER BY urls.id DESC;")
            urls = curs.fetchall()
            return urls


def add_url_by_name(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (url, datetime.now().date()))
            url_info = curs.fetchone()
            id_ = url_info.id
        conn.commit()
        return id_


def get_url_by_name(url):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE name = %s", (url,))
            url = curs.fetchone()
            return url


def get_url_by_id(id_):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s", (id_,))
            url = curs.fetchone()
            return url


def add_check(id_, status_code, title, h1, description):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                '''INSERT INTO url_checks
                (url_id, created_at, status_code, title, h1, description)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;''',
                (id_, datetime.now().date(), status_code, title, h1, description))
            check = curs.fetchone()
            id = check.id
        conn.commit()
        return id


def get_checks(id_):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC", (id_,))
            checks = curs.fetchall()
        conn.commit()
        return checks


def get_latest_check(id_):
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY created_at DESC LIMIT 1", (id_,))
            check_date = curs.fetchone()
        conn.commit()
        return check_date
