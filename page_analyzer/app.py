import os
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   get_flashed_messages,
                   redirect,
                   url_for)
from .validate import validate, normalize
import psycopg2
from .database import (get_all_urls,
                       get_url_by_name,
                       get_url_by_id)

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
    urls = get_all_urls(DATABASE_URL)
    return render_template('urls.html',
                           urls=urls)


@app.post('/urls')
def post_urls():
    url = request.form['url']
    errors = validate(url)

    if errors:
        if 'Url is empty' in errors:
            flash('Адрес сайта обязателен', 'error')
        elif 'Not valid url' in errors:
            flash('Некорректный адрес сайта', 'error')
        elif 'Url not found' in errors:
            flash('Адрес сайта не найден', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               url=url,
                               messages=messages), 422

    normalized_url = normalize(url)
    id_ = get_url_by_name(DATABASE_URL, normalized_url)
    flash('Адрес успешно добавлен', 'success')
    return redirect(url_for('show_url', id=id_))


@app.route('/urls/<int:id>', methods=['GET'])
def show_url(id):
    url = get_url_by_id(DATABASE_URL, id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        name=url.name,
        created_at=url.created_at,
        id=url.id,
        messages=messages)


if __name__ == '__main__':
    app.run()
