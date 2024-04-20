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

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET


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
    return render_template('show.html',
                           messages=messages,
                           urls=urls)


@app.route('/urls', methods=['POST'])
def post_urls():
    urls = request.form.to_dict().get('url', '')
    errors = validate(urls)

    if 'Url if empty' in errors:
        flash('Адрес сайта обязателен', 'error')
    if 'Not valid url' in errors:
        flash('Некорректный адрес сайта', 'error')
        return render_template('index.html'), 422

    cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (urls,))
    conn.commit()
    flash('Адрес успешно добавлен', 'success')
    return redirect(url_for('show_url', id=url_id)) #need to check the way of connect id.


@app.route('/urls/<int:id>')
def show_url(id):
    cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    url = cur.fetchone()
    return render_template(
        'show.html',
        url=url)
# need to add new html with all urls. And check other urls.

if __name__ == '__main__':
    app.run()
