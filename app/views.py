import json
from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, current_user
from app import app, db, oidc
from .forms import LoginForm
from .models import User


@app.before_request
def before_request():
    g.oidc = oidc

@app.route('/login/', methods=['GET', 'POST'])
@oidc.require_login
def login():
    email = g.oidc_id_token['email']
    if not email:
        return abort(404)
    session['email'] = email
    try:
        redirect(url_for('authorize_data'))
    except Exception as err:
        print err
    return redirect(url_for('authorize'))


@app.route('/logout/')
def logout():
    oidc.logout()
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    log = app.logger
    user_info = None
    if oidc.user_loggedin:
        user_info = oidc.user_getinfo(['name', 'email', 'exp', 'sub'])
        log.info('user is logged in: %s', user_info)
    else:
        log.info('No user is logged in: %s', user_info)
    return render_template('index.html',
                           title='Home',
                           user_info=user_info)


@app.route('/authorize/')
@oidc.require_login
def authorize():
    log = app.logger
    log.info('On endpoint: %s', request.path)
    user = oidc.user_getinfo(['name', 'family_name', 'email'])
    id_token = access_token = {}
    if oidc.credentials_store:
        credentials_dict = json.loads(oidc.credentials_store.values()[0])
        credentials_dict['id_token']['exp'] = datetime.fromtimestamp(credentials_dict['id_token']['exp']).strftime('%d-%b-%Y %H:%M:%S')
        id_token = credentials_dict['id_token']
        access_token = credentials_dict['token_response']
        log.info('Got credentials:')
        log.info('ID_TOKEN: %s', json.dumps(id_token, indent=4))
        log.info('ACCESS_TOKEN: %s', json.dumps({key:access_token[key] for key in access_token if key!='id_token'}, indent=4))
    return render_template('main.html',
                           title='Home',
                           user=user,
                           id_token = id_token,
                           access_token = access_token)

@app.route('/api/')
@oidc.accept_token(require_token=True)
def api():
    log = app.logger
    try:
        credentials_dict = json.loads(oidc.credentials_store.values()[0])
        access_token = credentials_dict['token_response']
        log.info('On endpoint: %s. Authenticated with token: %s',
                 request.path,
                 json.dumps({key:access_token[key] for key in access_token if key!='id_token'}, indent=4))
    except Exception as err:
        log.error('No local credentials found. Checking if the token is still active.')
    return json.dumps('Authenticated using token!')
