from app import app
from flask import render_template, request, redirect, session
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=["get", "post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        users.signup(username, password, role)
        return redirect("/")

@app.route("/login",methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template('error.html', message='Väärä käyttäjätunnus tai salasana')
        session['username'] = username
        return redirect('/')

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/')
