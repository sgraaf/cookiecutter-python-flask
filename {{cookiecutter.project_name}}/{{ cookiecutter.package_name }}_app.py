"""Create an application instance."""
from {{ cookiecutter.package_name }}.app import create_app

app = create_app()
