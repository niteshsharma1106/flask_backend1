# config.py

import os

# Set your database URI here
basepath = os.path.abspath(os.path.dirname(__file__)) #os.path.abspath(os.path.pardir)

DATABASE_URI = 'sqlite:///' + os.path.join(basepath, 'app.db')

print(DATABASE_URI)
SECRET_KEY = os.urandom(24)