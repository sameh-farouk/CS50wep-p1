CREATE TABLE
if not exists users
(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    emailAddress VARCHAR UNIQUE NOT NULL,
    password BYTEA NOT NULL,
    accountCreated TIMESTAMP DEFAULT current_timestamp,
    lastSeen TIMESTAMP
);
CREATE TABLE
if not exists books
(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publication_year smallint Not Null,
    added TIMESTAMP DEFAULT current_timestamp
);
CREATE TABLE
if not exists reviews
(
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE RESTRICT,
    rating NUMERIC(3,2) NOT NULL,
    text TEXT NOT NULL,
    added TIMESTAMP DEFAULT current_timestamp,
    UNIQUE (book_id, user_id)
);