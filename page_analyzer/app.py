import os
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   get_flashed_messages,
                   redirect,
                   url_for)
from .validate import validate
import psycopg2


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print('Connection to database established successfully!')
except Exception as e:
    print(f'Failed to connect to database: {e}')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    cur.execute("SELECT * FROM urls")
    urls = cur.fetchall()
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls.html',
                           messages=messages,
                           urls=urls)


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    errors = validate(url)

    if errors:
        if 'Url if empty' in errors:
            flash('Адрес сайта обязателен', 'error')
        elif 'Not valid url' in errors:
            flash('Некорректный адрес сайта', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               url=url,
                               messages=messages), 422

    cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (url,))
    conn.commit()
    flash('Адрес успешно добавлен', 'success')
    return redirect(url_for('show_url', id=url_id)) #need to check the way of connect id.


@app.route('/urls/<int:id>')
def show_url(id):
    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    url = cur.fetchone()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url=url,
        messages=messages)
# need to add new html with all urls. And check other urls.

if __name__ == '__main__':
    app.run()
