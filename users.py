from db import db
#from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = 'select id, username, password, role from users where username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user['password']
        if check_password_hash(hash_value, password):
            return True
        return False

def signup(username, password, role):
    hash_value = generate_password_hash(password)
    sql = 'insert into users (username, password, role) values (:username, :password, :role)'
    db.session.execute(
        sql, {'username': username, 'password': hash_value, 'role': role}
    )
    db.session.commit()

