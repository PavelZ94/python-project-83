import os
import requests
from requests.exceptions import RequestException
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   get_flashed_messages,
                   redirect,
                   url_for)
from .validate import validate, normalize
from .parser import parser
from .database import (connection,
                       get_all_urls,
                       add_url_by_name,
                       get_url_by_id,
                       get_url_by_name,
                       add_check,
                       get_checks,
                       get_latest_check)


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

try:
    with connection() as conn:
        cur = conn.cursor()
        print('Connection to database established successfully!')
except Exception as e:
    print(f'Failed to connect to database: {e}')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    urls = get_all_urls()
    checks = {url.id: get_latest_check(url.id) for url in urls}
    return render_template('urls.html',
                           urls=urls,
                           checks=checks)


@app.post('/urls')
def post_urls():
    url = request.form['url']
    errors = validate(url)

    if errors:
        if 'Url is empty' in errors:
            flash('Адрес сайта обязателен', 'danger')
        elif 'Not valid url' in errors:
            flash('Некорректный URL', 'danger')
        elif 'Url not found' in errors:
            flash('Адрес сайта не найден', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               url=url,
                               messages=messages), 422

    normalized_url = normalize(url)
    dublicate = get_url_by_name(normalized_url)
    if dublicate:
        id_ = dublicate.id
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=id_))

    else:
        id_ = add_url_by_name(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=id_))


@app.route('/urls/<int:id>')
def show_url(id):
    url = get_url_by_id(id)
    checks = get_checks(id)
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
    url = get_url_by_id(id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    status_code, title, h1, description_content = parser(response)
    add_check(id, status_code, title, h1, description_content)
    return redirect(url_for('show_url', id=id))


if __name__ == '__main__':
    app.run()
