from flask import (
        redirect, request, Blueprint, session, abort, g, flash, render_template, url_for
    )

from stackapi import StackAPI
import urllib.request, urllib.parse
import time
import pprint


from google.cloud.datastore import key, entity
from . import db


bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = "Please input an username"
        elif not password:
            error= "Please input a password"
        else:
            database = db.start_db()
            user_entity = db.query_user(database, username)
            if user_entity:
                error = "User is registered"
            else: 
                import bcrypt
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                db.add_user(database, username, hashed_password) 
                return redirect(url_for('.login'))
        flash(error)

    return render_template('register.html')

@bp.route('/login', methods=('POST','GET'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = "Please input an username"
        elif not password:
            error = "Please input a password"
        else:
            database = db.start_db()
            user_entity = db.query_user(database, username)
            if not user_entity:
                error = "User not registered"
            else:
                hashed_password = db.query_pass(database, username, password)
                print(hashed_password)
                import bcrypt
                if bcrypt.hashpw(password.encode("utf-8"), hashed_password) == hashed_password:
                    return redirect(url_for('index'))
                else:
                    error = "Wrong user/password combination"
                

        flash(error)
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def get_loaded_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user=None
    else:
        #TODO
        pass 
