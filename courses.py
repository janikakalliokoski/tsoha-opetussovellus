from secrets import choice
from db import db
from random import choice

def add_course(name, questions, teacher_id):
    sql = "insert into courses (name, teacher_id, visible) values (:name, :teacher_id, 1) returning id"
    course_id = db.session.execute(sql, {"name":name, "teacher_id":teacher_id}).fetchone()[0]

    for i in questions.split("\n"):
        parts = i.strip().split(";")
        if len(parts) != 2:
            continue

        sql = "insert into questions (course_id, question, answer) values (:course_id, :question, :answer)"
        db.session.execute(sql, {"course_id":course_id, "question":parts[0], "answer":parts[1]})

    db.session.commit()
    return course_id

def get_all_courses():
    sql = "select id, name from courses where visible=1 order by name"
    return db.session.execute(sql).fetchall()

def get_course_info(course_id):
    sql = """select c.name, u.username from courses c, users u
             where c.id=:course_id and c.teacher_id=u.id"""
    return db.session.execute(sql, {"course_id": course_id}).fetchone()

def get_question(course_id):
    sql = "select id, question from questions where course_id=:course_id order by id"
    result = list(db.session.execute(sql, {"course_id": course_id}).fetchall())
    questions = []
    for i in result:
        questions.append(i)
    return questions

def get_question_info(question_id):
    sql = "select course_id, question from questions where id=:question_id"
    return db.session.execute(sql, {"question_id": question_id}).fetchone()

def get_questions(question_id):
    sql = "select question, answer from questions where id=:question_id"
    return db.session.execute(sql, {"question_id":question_id}).fetchone()

def submit_answer(question_id, answer, user_id):
    sql = "select answer from questions where id=:id"
    correct = db.session.execute(sql, {"id":question_id}).fetchone()[0]

    result = 1 if answer == correct else 2

    sql = "insert into answers (user_id, question_id, sent, result) values (:user_id, :question_id, now(), :result)"
    db.session.execute(sql, {"user_id":user_id, "question_id":question_id, "result":result})
    db.session.commit()
