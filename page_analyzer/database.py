import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from typing import NamedTuple
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


def connection():
    """
    Connect to the database and return the connection object.

    Returns:
        psycopg2.connection: Connection object if successful, None otherwise
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print('Connection to database established successfully!')
        return conn
    except Exception as e:
        print(f'Failed to connect to database: {e}')
        return None


def get_all_urls() -> list:
    """
    Retrieve all URLs from the database in descending order of their IDs.

    Returns:
        list: A list of named tuples representing URLs,
    ordered by ID in descending order.

    Raises:
        Exception: An error occurred while retrieving the URLs
        from the database.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls ORDER BY urls.id DESC;")
            urls = curs.fetchall()
            return urls


def add_url_by_name(url: str) -> int:
    """
    Add information about a URL to the database if it doesn't already exist.

    Args:
        url (str): The name of the URL to add.

    Returns:
        int: The ID of the added URL to redirect to its dedicated page.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                '''INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id;''',
                (url, datetime.now().date()))
            url_info = curs.fetchone()
            id_ = url_info.id
        conn.commit()
        return id_


def get_url_by_name(url: str) -> NamedTuple:
    """
    Retrieve a URL from the database by its name.

    Args:
        url (str): The name of the URL to retrieve.

    Returns:
        namedtuple: Information about the given URL from the database.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE name = %s", (url,))
            url = curs.fetchone()
            return url


def get_url_by_id(id_: int) -> NamedTuple:
    """
    Retrieve information about a URL by its ID from the database.

    Args:
        id_ (int): The ID of the URL to retrieve.

    Returns:
        namedtuple: Information about the URL with the given ID
        from the database.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s", (id_,))
            url = curs.fetchone()
            return url


def add_check(
        id_: int,
        status_code: int,
        title: str,
        h1: str,
        desc: str
) -> int:
    """
    Add information about a URL check performed.

    Args:
        id_ (int): The ID of the URL being checked.
        status_code (int): The HTTP status code of the check.
        title (str): The title parsed from the URL.
        h1 (str): The h1 header from the URL.
        desc (str): The meta description from the URL.

    Returns:
        int: The ID of the added URL check.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                '''INSERT INTO url_checks
                (url_id, created_at, status_code, title, h1, description)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;''',
                (id_, datetime.now().date(),
                 status_code, title, h1, desc))
            check = curs.fetchone()
            check_id = check.id
        conn.commit()
        return check_id


def get_checks(id_: int) -> list:
    """
    Retrieve information about completed checks on a URL's page.

    Args:
        id_ (int): The ID of the URL to retrieve checks for.

    Returns:
        list: A list of named tuples representing completed checks on the URL,
        ordered by ID in descending order.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''SELECT *
            FROM url_checks
            WHERE url_id=%s ORDER BY id DESC''', (id_,))
            checks = curs.fetchall()
        conn.commit()
        return checks


def get_latest_check(id_: int) -> NamedTuple:
    """
    Retrieve information about the latest completed check of a URL
    with the given ID.

    Args:
        id_ (int): The ID of the URL to retrieve the latest check for.

    Returns:
        namedtuple: Information about the latest completed check of the URL.
    """
    with connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''SELECT *
            FROM url_checks
            WHERE url_id=%s ORDER BY created_at DESC LIMIT 1''', (id_,))
            check_date = curs.fetchone()
        conn.commit()
        return check_date
