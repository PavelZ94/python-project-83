# Page analyzer


### Hexlet tests and linter status:
[![Actions Status](https://github.com/PavelZ94/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/PavelZ94/python-project-83/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/61f0e2eabfe9d87580cf/maintainability)](https://codeclimate.com/github/PavelZ94/python-project-83/maintainability)

[![Lint_check](https://github.com/PavelZ94/python-project-83/actions/workflows/lint_check.yml/badge.svg)](https://github.com/PavelZ94/python-project-83/actions)

## About

The Page Analyzer is an application based on the Flask framework. Here, the basic principles of building modern websites on the MVC architecture are worked out: working with routing, query handlers and a template engine, interacting with a database.
Page Analyzer is a website that analyzes the specified pages for SEO suitability

## Stack

To install and use an application you should have:
- python = "^3.11"
- gunicorn = "^21.2.0"
- flask = "^3.0.3"
- python-dotenv = "^1.0.1"
- psycopg2-binary = "^2.9.9"
- validators = "^0.28.0"
- requests = "^2.31.0"
- bs4 = "^0.0.2"
- beautifulsoup4 = "^4.12.3"
- lxml = "^5.2.1"
- flake8 = "^7.0.0"

The project also uses PostgreSQL as a relational database management system.

## Installation

Make sure you installed the latest versions of all programs before using application.
To install programs you should use this command:
```
pip install "name of program"
```
To check version of program use this command:
```
"name of program" --version
```
After you are sure that all programs are installed follow these steps:
1) Firstly you should clone repository to your local machine:
```
git clone git@github.com:PavelZ94/python-project-83.git
```
2) Next you should install necessary dependencies:
```
make install
```
3) Then create .env file with information about database and secret key:
```
DATABASE_URL = "{provider}://{user}:{password}@{host}:{port}/{db}"
SECRET_KEY = "your secret key"
```
when:
- provider - Your relational database management system ('postgresql' in this case);
- user - database creator in postgresql;
- password - password of user;
- host - host on which the project will be launched (default='localhost');
- port - default='5432';
- db - name of your database in postgresql.

## Usage

To launch the application use command:
```
make start
```
It will launch application on default host and port: http://0.0.0.0:8000/

Also, you can launch it in development mode with debugger active using:
```
make dev
```
This case it will be launched http://127.0.0.1:5432/ as default if you used parameters `'localhost'` and port `'5432'` in instruction above.

In application, you can add new URL in form on main page and click the button `"ПРОВЕРИТЬ"`.

Then, if URL is correct, it will redirect you to its URL page. Now you can launch check by pushing button `"ЗАПУСТИТЬ ПРОВЕРКУ"`. 
if the check was successful, a row with the check id, page status code, header data, descriptions, and the date of check will be added to the table.

Any successful action in the application is accompanied by a flash message. They are displayed at the top of the screen. Keep an eye on their content.

You can go to the page with all the verified addresses at any time.
To do this, click on the button `"САЙТЫ"` at the top of the screen.

It will show information about all URLS that have been checked, the status codes of their last check and its date are indicated.

## The result of deploy

https://python-project-83-6d0w.onrender.com
