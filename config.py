# config.py

import os

# Set your database URI here
basepath = os.path.abspath(os.path.pardir)

DATABASE_URI = 'sqlite:///'+basepath+'app.db'
SECRET_KEY = os.urandom(24)