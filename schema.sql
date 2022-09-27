create table users (
    id serial primary key,
    username text unique,
    password text,
    role text
);
