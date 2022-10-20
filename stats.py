from db import db

def get_course_stats(user_id):
    sql = """select id, name from courses
             where teacher_id=:user_id and visible=1 order by name"""
    courses = db.session.execute(sql, {"user_id": user_id}).fetchall()

    data = []
    for course in courses:
        sql = """select coalesce(count(*),0) from answers a, questions q
                 where q.course_id=:course_id and a.question_id=q.id"""
        result = str(db.session.execute(sql, {"course_id": course[0]}).fetchone())
        total = []
        for i in result:
            total.append(i)
        total.pop(0)
        total.pop(-1)
        total.pop(-1)
        total = "".join(total)
        sql = """select coalesce(sum(a.result),0) from answers a, questions q
                 where q.course_id=:course_id and a.question_id=q.id"""
        res = str(db.session.execute(sql, {"course_id": course[0]}).fetchone())
        print(res)
        correct = []
        for i in res:
            correct.append(i)
        correct.pop(0)
        correct.pop(-1)
        correct.pop(-1)
        correct = "".join(correct)
        sql = """select u.username, q.title, a.result
                 from answers a, questions q, users u
                 where q.course_id=:course_id and a.question_id=q.id and u.id=a.user_id
                 group by q.title, u.username, a.result order by u.username"""
        results = db.session.execute(sql, {"course_id": course[0]}).fetchall()
        data.append((course[1], int(total), int(correct), results))

    return data
