DROP TABLE IF EXISTS Clocking;

DROP TABLE IF EXISTS Users;

PRAGMA foreign_keys = ON;

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL CHECK(LENGTH(username)>{} AND LENGTH(username)<{}),
    salt_password BLOB NOT NULL,
    email TEXT UNIQUE CHECK(LENGTH(email)>{} AND LENGTH(email)<{}),
    is_admin INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1
    );

CREATE TABLE Clocking (
    user_id,
    clock_in TEXT NOT NULL,
    clock_out TEXT DEFAULT NULL,
    comment TEXT DEFAULT "",
    FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
    );