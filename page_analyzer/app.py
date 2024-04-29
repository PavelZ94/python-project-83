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
                       add_url_by_name,
                       get_url_by_id,
                       get_url_by_name,
                       add_check,
                       get_checks,
                       get_latest_check)

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
    checks = {url.id: get_latest_check(DATABASE_URL, url.id) for url in urls}
    return render_template('urls.html',
                           urls=urls,
                           checks=checks)


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
    dublicate = get_url_by_name(DATABASE_URL, normalized_url)
    if dublicate:
        flash('Адрес уже добавлен', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               messages=messages), 422

    else:
        id_ = add_url_by_name(DATABASE_URL, normalized_url)
        flash('Адрес успешно добавлен', 'success')
        return redirect(url_for('show_url', id=id_))


@app.route('/urls/<int:id>')
def show_url(id):
    url = get_url_by_id(DATABASE_URL, id)
    checks = get_checks(DATABASE_URL, id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        name=url.name,
        created_at=url.created_at,
        id=url.id,
        messages=messages,
        checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_post(id):
    check_id = add_check(DATABASE_URL, id)

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))


if __name__ == '__main__':
    app.run()
