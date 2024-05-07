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
from .database import (get_all_urls,
                       add_url_by_name,
                       get_url_by_id,
                       get_url_by_name,
                       add_check,
                       get_checks,
                       get_latest_check)


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    """
    Render main page.
    """
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    """
    Render the page with all added URLs.
    Contains the table with:
    - id of URL;
    - the Name of URL;
    - the date of last check;
    - status code of last check.
    """
    urls = get_all_urls()
    checks = {url.id: get_latest_check(url.id) for url in urls}
    return render_template('urls.html',
                           urls=urls,
                           checks=checks)


@app.post('/urls')
def post_urls():
    """
    Add new URL. Validate the entered URL for correctness.
    If it's not correct, or empty,
    it's redirecting to main page with flash message of error.
    If the URL was entered before, it's redirecting to the page of this URL.
    Otherwise, the URL is added, and it's redirecting to the page of this URL.
    """
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
    """
    Render the page of URL.
    Contains two tables with information about URL:
    First table:
    - id of URL;
    - name of URL;
    - date, when URL was added to database.

    Second table:
    - check id;
    - status code of check;
    - h1 parsed from URL;
    - title parsed from URL;
    - description parsed from URL meta;
    - date of completed check.
    """
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
    """
    Check requested URL. Add the information of completed check to database.
    If check is successful redirect to the page of URL
    with information of completed check.
    If check is not successful redirect to the same page
    with error message during check.
    """
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


@app.errorhandler(404)
def page_not_found(error):
    """
    Render 404 error page if requested page is missing.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """
    Render 500 error if unable to connect server.
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
