import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

requirements = [
"alembic==1.13.2",
"atomicwrites==1.4.1",
"attrs==21.2.0",
"blinker==1.8.2",
"click==8.1.7",
"coverage==7.6.1",
"Flask==2.0.1",
"Flask-Alembic==2.0.1",
"Flask-Migrate==3.1.0",
"Flask-SQLAlchemy==2.4.4",
"greenlet==3.1.1",
"gunicorn==20.1.0",
"importlib-resources==5.2.2",
"iniconfig==1.1.1",
"itsdangerous==2.2.0",
"Jinja2==3.1.4",
"Mako==1.3.5",                                                   
"MarkupSafe==2.1.5",
"marshmallow==3.13.0",
"marshmallow-enum==1.5.1",
"marshmallow-sqlalchemy==0.26.1",
"packaging==21.0",
"py==1.10.0",
"pyparsing==2.4.7",
"pytest==6.2.5",
"pytest-cov==2.12.1",
"setuptools==75.1.0",
"SQLAlchemy==1.4.47",
"toml==0.10.2",
"typing_extensions==4.12.2",
"Werkzeug==2.0.2",
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