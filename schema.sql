create table users (
    id serial primary key,
    username text unique,
    password text,
    role text
);

create table courses (
    id serial primary key,
    teacher_id integer references users,
    name text,
    visible integer
);

create table questions (
    id serial primary key,
    course_id integer references courses,
    question text,
    answer text
);

create table answers (
    id serial primary key,
    user_id integer references users,
    question_id integer references questions,
    sent timestamp,
    result integer
);