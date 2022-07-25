import os
import subprocess
import sys
from pathlib import Path

root_dir = Path.cwd()
venv_dir = root_dir / ".venv"

if os.name == "posix":
    python_executable = r".venv/bin/python"
else:
    python_executable = r".venv\Scripts\python"


def init_venv():
    # create venv
    subprocess.run([sys.executable, "-m", "venv", ".venv"])

    # install requirements
    subprocess.run(
        [python_executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools"]
    )
    subprocess.run(
        [python_executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]
    )


def init_db():
    # check if venv exists
    if not venv_dir.is_dir():
        raise RuntimeError("You cannot use `init_db` without `init_venv`.")

    # perform revision and upgrade
    subprocess.run(
        [
            python_executable,
            "-m",
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            "🍪 Initial revision from cookiecutter -- add `users` table",
        ]
    )
    subprocess.run([python_executable, "-m", "alembic", "upgrade", "head"])

    # seed the database
    subprocess.run([python_executable, "-m", "flask", "db", "seed"])


def init_git():
    # initialize git repository
    subprocess.run(["git", "init", "-b", "main"])

    # install pre-commit hooks
    subprocess.run(["pre-commit", "install"])

    # add initial commit
    subprocess.run(["git", "add", "."])
    subprocess.run(["pre-commit", "run", "--all-files"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "🍪 Initial commit from cookiecutter"])


if __name__ == "__main__":
    if "{{ cookiecutter.init_venv }}" == "True":  # initialize virtual environment
        init_venv()
    if "{{ cookiecutter.init_db }}" == "True":  # initialize database
        init_db()
    if "{{ cookiecutter.init_git }}" == "True":  # initialize git repository
        init_git()
