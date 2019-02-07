from flask import (
        redirect, request, Blueprint, session, abort, g, flash, render_template, url_for
    )

import time
import pprint


from google.cloud.datastore import key, entity
from . import db
from .settings import auth


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
                    return redirect(url_for('auth.stackexchange_auth', scope='no_expiry'))
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


@bp.route('/<scope>/stackexchange_auth', methods=('GET', 'POST'))
def stackexchange_auth(scope):
    if request.method=='GET':
        stack_url = 'https://stackoverflow.com/oauth?scope={scope}&client_id={client_id}&redirect_uri={redirect_uri}'
        return redirect(stack_url.format(client_id=auth.client_id,
                                         scope=scope,
                                         redirect_uri=auth.root_uri + url_for('auth.redirect_flow', token="None")
                                         ))

@bp.route('/<token>/redirect_flow', methods=('GET', 'POST'))
def redirect_flow(token):
    if request.args.get("code") is not None:
        headers={"Content-Type": "application/x-www-form-urlencoded"}
        data={
            "client_id": auth.client_id,
            "client_secret": auth.client_secret,
            "redirect_uri": auth.root_uri + url_for('auth.redirect_flow', token="None"),
            "code": request.args.get("code")
            }
        print(data["code"])
        import urllib.request, urllib.parse
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request("https://stackoverflow.com/oauth/access_token", headers=headers, data=data)
        time.sleep(1)
        res = urllib.request.urlopen(req)
        return redirect(url_for("auth.redirect_flow", token=res.read().decode("UTF-8")))

    else:
        return redirect(url_for("stack.api.api_query", token=token))

