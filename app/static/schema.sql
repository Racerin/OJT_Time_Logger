PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Users (
user_id INTEGER PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
salt_password BLOB NOT NULL,
email TEXT UNIQUE,
is_admin INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Clock (
user_id,
clock_in TEXT NOT NULL,
clock_out TEXT,
comment TEXT,
FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create admin account
INSERT INTO Users VALUES(
'admin',
x'\xda1Y[D\xa3Yg"\x0f\xd3\x1b\x83\xd7R\xe80o\xb2\xeeu;7\xe3\xd6\xfd%\x0b4~x\x92',
'drsbaird@yahoo.com',
1
);

-- Create dumby user
INSERT INTO Users VALUES(
'FooBar', 
x'\x86\x98\xc8/=\x121\xd0\xf5E\xf0\x1b\xba\x17\xec\xe5\x0eG\xd3\x11\xc5O\xef\xf7\xbe\xd3\xa5\x80\x10\x85\xe6^', 
'example@example.com'
);