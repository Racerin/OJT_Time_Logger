DROP TABLE IF EXISTS Clocking;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    salt_password BLOB NOT NULL,
    email TEXT UNIQUE,
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