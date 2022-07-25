import re
import sys

PACKAGE_REGEX_PATTERN = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9]+$")

package_name = "{{ cookiecutter.package_name }}"


def check_python_version():
    python_major_version = sys.version_info[0]
    python_minor_version = sys.version_info[1]

    if (python_major_version == 2) or (
        python_major_version == 3 and python_minor_version < 7
    ):
        raise RuntimeError(
            "You are running cookiecutter using Python {python_major_version}.{python_minor_version}, but a version >= Python 3.7 is required.".format(
                python_major_version=python_major_version,
                python_minor_version=python_minor_version,
            )
        )


def validate_package_name():
    if not PACKAGE_REGEX_PATTERN.match(package_name):
        raise ValueError(
            f"Invalid package name: `{package_name}`. Please only use alphanumerics and underscores (_). See https://peps.python.org/pep-0008/#package-and-module-names for more information on package and module naming standards."
        )


if __name__ == "__main__":
    check_python_version()
    validate_package_name()
