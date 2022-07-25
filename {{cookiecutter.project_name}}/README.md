# {{ cookiecutter.friendly_name }}

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

> {{ cookiecutter.description }}

## Run

```bash
flask run
```

## Database

### Migrations

```bash
flask db migrate revision --autogenerate -m "Revision message"
flask db migrate upgrade head
```

### Seeding

```bash
flask db seed
```
