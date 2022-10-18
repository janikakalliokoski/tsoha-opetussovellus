from db import db

def add_course(name, questions, teacher_id):
    sql = "insert into courses (name, teacher_id, visible) values (:name, :teacher_id, 1) returning id"
    course_id = db.session.execute(sql, {"name":name, "teacher_id":teacher_id}).fetchone()[0]

    for i in questions.split("\n"):
        parts = i.strip().split(";")
        if len(parts) != 3:
            continue

        sql = "insert into questions (course_id, title, question, answer) values (:course_id, :title, :question, :answer)"
        db.session.execute(sql, {"course_id":course_id, "title":parts[0], "question":parts[1], "answer":parts[2]})

    db.session.commit()
    return course_id


def add_material(course_id, material):
    sql = "insert into materials (course_id, material) values (:course_id, :material)"
    db.session.execute(sql, {"course_id":course_id, "material":material})
    db.session.commit()

def delete_course(course_id, user_id):
    sql = "update courses set visible=0 where id=:id and teacher_id=:user_id"
    db.session.execute(sql, {"id":course_id, "user_id":user_id})
    db.session.commit()

def delete_course_material(course_id):
    sql = "delete from materials where course_id=:course_id"
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()

def get_course_material(course_id):
    sql = "select material from materials where course_id=:course_id"
    result = str(db.session.execute(sql, {"course_id":course_id}).fetchone())
    material = []
    for i in result:
        material.append(i)
    material.pop(0)
    material.pop(0)
    material.pop(-1)
    material.pop(-1)
    material.pop(-1)
    real = "".join(material)
    return real

def get_all_courses():
    sql = "select id, name from courses where visible=1 order by name"
    return db.session.execute(sql).fetchall()

def get_course_info(course_id):
    sql = "select c.name, u.username from courses c, users u where c.id=:course_id and c.teacher_id=u.id"
    return db.session.execute(sql, {"course_id": course_id}).fetchone()

def get_own_courses(user_id):
    sql = "select id, name from courses where teacher_id=:user_id and visible = 1 order by id"
    result = list(db.session.execute(sql, {"user_id":user_id}).fetchall())
    courses = []
    for course in result:
        courses.append(course)
    return courses

def get_question(course_id):
    sql = "select id, title, question from questions where course_id=:course_id order by id"
    result = list(db.session.execute(sql, {"course_id": course_id}).fetchall())
    questions = []
    for i in result:
        questions.append(i)
    return questions

def get_question_info(question_id):
    sql = "select course_id, title, question from questions where id=:question_id"
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
