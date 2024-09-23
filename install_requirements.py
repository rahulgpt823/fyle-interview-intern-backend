import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

requirements = [
    "alembic==1.7.1",
    "atomicwrites==1.4.1",
    "attrs==21.2.0",
    "blinker==1.8.2"
    "click==8.0.1",
    "colorama==0.4.6"
    "coverage==5.5",
    "Flask==2.0.1",
    "Flask-Alembic==2.0.1",
    "Flask-Migrate==3.1.0",
    "Flask-SQLAlchemy==2.5.1",
    "greenlet==3.1.1",
    "gunicorn==20.1.0",
    "importlib-resources==5.2.2",
    "iniconfig==1.1.1",
    "itsdangerous==2.0.1",
    "Jinja2==3.0.1",
    "Mako==1.1.5",
    "MarkupSafe==2.0.1",
    "marshmallow==3.13.0",
    "marshmallow-enum==1.5.1",
    "marshmallow-sqlalchemy==0.26.1",
    "packaging==21.0",
    "pip==24.2",
    "pluggy==1.5.0",
    "pyparsing==2.4.7",
    "pytest==8.3.3",
    "pytest-cov== 5.0.0",
    "pytest-html==4.1.1",
    "pytest-metadata==3.1.1",
    "setuptools==75.1.0"
    "SQLAlchemy==1.4.23",
    "toml==0.10.2",
    "typing_extensions==4.12.2",
    "Werkzeug==2.0.1",
    "zipp==3.5.0",
    "zope.event==4.5.0",
    "zope.interface==5.4.0"
]

for req in requirements:
    print(f"Installing {req}")
    try:
        install(req)
    except subprocess.CalledProcessError:
        print(f"Failed to install {req}")

print("Installation complete. Please check for any error messages above.")