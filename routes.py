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
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Käyttäjänimen on oltava 1-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if len(password1) < 8 or len(password1) > 20:
            return render_template("/error.html", message="Salasanan on oltava 8-20 merkkiä")

        role = request.form["role"]

        if users.signup(username, password1, role):
            return render_template("index.html", message=f"Käyttäjä {username} luotu onnistuneesti!")
        else:
            return render_template("error.html", message="Käyttäjän luonti ei onnistunut, kokeile toista käyttäjänimeä")

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
