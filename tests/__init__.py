# from core.server import app
# app.testing = True
from core import create_app, db

app = create_app('test')