BEGIN;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS calendars CASCADE;
DROP TABLE IF EXISTS access_rights CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS events CASCADE;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    realname TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
CREATE TABLE calendars (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users,
    name TEXT,
    private BOOLEAN NOT NULL DEFAULT true
);
CREATE TABLE access_rights (
    calendar_id INTEGER REFERENCES calendars,
    user_id INTEGER REFERENCES users,
    view_calendar BOOLEAN NOT NULL,
    modify_calendar BOOLEAN NOT NULL,
    change_rights BOOLEAN NOT NULL,
    delete_calendar BOOLEAN NOT NULL
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    calendar_id INTEGER REFERENCES calendars,
    name TEXT NOT NULL,
    description TEXT
);
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    name TEXT NOT NULL,
    description TEXT
);
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs,
    calendar_id INTEGER REFERENCES calendars,
    name TEXT NOT NULL,
    description TEXT,
    planned_time INTEGER DEFAULT 0
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    planned_time INTEGER,
    actual_time INTEGER
);
COMMIT;