from app import app
from flask import render_template, request, redirect
import users
import courses

@app.route("/")
def index():
    return render_template("index.html", courses=courses.get_all_courses())

@app.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Käyttäjänimen on oltava 1-20 merkkiä")
        if " " in username:
            return render_template("error.html", message="Käyttäjänimi ei voi sisältää välilyöntejä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if " " in password1:
            return render_template("error.html", message="Salasana ei voi sisältää välilyöntejä")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if len(password1) < 8 or len(password1) > 20:
            return render_template("/error.html", message="Salasanan on oltava 8-20 merkkiä")

        role = request.form["role"]

        if users.signup(username, password1, role):
            return render_template("index.html", message=f"Käyttäjä {username} luotu onnistuneesti!")
        else:
            return render_template("error.html", message="Käyttäjän luonti ei onnistunut, kokeile toista käyttäjänimeä")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")
    else:
        return render_template("error.html", message="Uloskirjautuminen ei onnistunut")

@app.route("/create", methods=["GET", "POST"])
def create_course():
    users.require_role("2")

    if request.method == "GET":
        return render_template("create.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Kurssin nimen on oltava 1-20 merkkiä")
        if " "*len(name) == name:
            return render_template("error.html", message="Kurssin nimen tulee sisältää muita kuin pelkkiä välilyöntejä")
        if "" == name:
            return render_template("error.html", message="Kurssin nimi ei voi olla tyhjä")

        material = request.form["material"]
        if len(material) < 1 or len(material) > 500:
            return render_template("error.html", message="Linkin tulee olla 1-500 merkkiä pitkä")
        if " "*len(material) == material:
            return render_template("error.html", message="Linkin tulee sisältää muita kuin pelkkiä välilyöntejä")
        if "" == material:
            return render_template("error.html", message="Linkki ei voi olla tyhjä")

        questions = request.form["words"]
        if len(questions) > 10000:
            return render_template("error.html", message="Kysymys/vastauspareja on liikaa")

        course_id = courses.add_course(name, questions, users.user_id())
        courses.add_material(course_id, material)
        return redirect("/course/"+str(course_id))

@app.route("/course/<int:course_id>")
def show_course(course_id):
    info = courses.get_course_info(course_id)
    material = courses.get_course_material(course_id)

    questions = []

    for question in courses.get_question(course_id):
        questions.append(question)

    return render_template("course.html", course_id=course_id, name=info[0], teacher=info[1], material=material, size=len(questions), questions=questions)

@app.route("/question/<int:question_id>")
def show_question(question_id):
    info = courses.get_question_info(question_id)

    return render_template("question.html", question=info[2], question_id=question_id, course_id=info[0])

@app.route("/result", methods=["POST"])
def result():
    course_id = request.form["course_id"]
    question_id = request.form["question_id"]
    answer = request.form["answer"].strip()

    courses.submit_answer(question_id, answer, users.user_id())
    questions = courses.get_questions(question_id)

    return render_template("result.html", course_id=course_id, question=questions[0], answer=answer, correct=questions[1])
