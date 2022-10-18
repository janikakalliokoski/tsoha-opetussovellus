from db import db
from flask import session, abort, request
import os
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "select id, username, password, role from users where username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["user_username"] = username
        session["user_role"] = user[3]
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def logout():
    try:
        session.pop("user_id", None)
        session.pop("user_username", None)
        session.pop("user_role", None)
    except:
        return False
    return True

def user_id():
    return session.get("user_id", 0)

def signup(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "insert into users (username, password, role) values (:username, :password, :role)"
        db.session.execute(
            sql, {"username": username, "password": hash_value, "role": role}
        )
        db.session.commit()
    except:
        return False
    return True

def require_role(role):
    if role != session.get("user_role", 0):
        abort(403)

def all_users():
    sql = "select id, username from users"
    users = db.session.execute(sql).fetchall()
    return users

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)