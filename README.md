# cookiecutter-python-flask

[![Supported Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue)](https://github.com/sgraaf/cookiecutter-python-flask)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

> A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) project template for Python Flask projects.

## Usage

```bash
cookiecutter https://github.com/sgraaf/cookiecutter-python-flask.git
```

## Features

-   Configuration in environment variables, as per [The Twelve-Factor App](https://12factor.net/config)
-   Utilizes best practices, such as [Blueprints](https://flask.palletsprojects.com/en/2.1.x/blueprints/) and [Application Factories](https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/)
-   ORM via [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy) with a (basic) User model
-   Easy database management via [Flask-DB](https://github.com/nickjj/flask-db)
-   Forms via [Flask-WTF](https://github.com/wtforms/flask-wtf/) with login, registration and password reset forms
-   E-mail sending via [Flask-Mail](https://github.com/mattupstate/flask-mail)
-   User session management (i.e. authentication) via [Flask-Login](https://github.com/maxcountryman/flask-login)
-   Strong password hashing via [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt)
-   Date and time formatting using [Moment.js](https://momentjs.com/) via [Flask-Moment](https://github.com/miguelgrinberg/flask-moment)
-   Bootstrap 5 via [Bootstrap-Flask](https://github.com/helloflask/bootstrap-flask) with starter templates
-   Linting with [pre-commit](https://pre-commit.com/) and [flake8](http://flake8.pycqa.org/)
-   Code formatting with [isort](https://pycqa.github.io/isort/), [black](https://black.readthedocs.io/en/stable/) and [Prettier](https://prettier.io/)
-   Type checking with [mypy](http://mypy-lang.org/)
-   Remove unused imports with [autoflake](https://github.com/PyCQA/autoflake)
-   Import sorting with [isort](https://pycqa.github.io/isort/)
-   Automatic Python syntax upgrades with [pyupgrade](https://github.com/asottile/pyupgrade)
-   Automatic git initialization
-   Automatic virtual environment creation
-   Automatic requirements installation

This template supports Python 3.7, 3.8, 3.9 en 3.10.
