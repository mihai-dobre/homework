import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oidc import OpenIDConnect, MemoryCredentials

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)

oidc = OpenIDConnect(app, {})

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('log/homework.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    print app.logger_name
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('homework start')
    f_oidc = logging.getLogger('flask_oidc')
    f_oidc.addHandler(file_handler)

# to avoid the circular import
from app import views, models