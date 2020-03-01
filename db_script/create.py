import sqlite3

db = sqlite3.connect('../database.db')
cur = db.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS User_Auth;

CREATE TABLE Users(
    UUID CHAR(16) PRIMARY KEY NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    forename VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL
);

CREATE TABLE User_Auth(
    UUID CHAR(16) PRIMARY KEY NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    FOREIGN KEY (UUID) REFERENCES Users(UUID)
);
    

CREATE TABLE Posts(
    id INTEGER PRIMARY KEY NOT NULL,
    heading VARCHAR(512) NOT NULL,
    body TEXT,
    username VARCHAR(255) NOT NULL,
    date_posted DATE NOT NULL,
    time_posted TIME NOT NULL,
    FOREIGN KEY (username) REFERENCES Users(username)
);

CREATE TABLE Comments(
    id INTEGER PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL,
    postid INTEGER NOT NULL,
    date_posted DATE NOT NULL,
    time_posted TIME NOT NULL,
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (postid) REFERENCES Posts(id)
);



CREATE OR replace FUNCTION Authenticate_User (_username VARCHAR, _password VARCHAR)
RETURNS boolean AS $$
declare
    records INTEGER;
begin
    SELECT COUNT(Users.UUID) INTO records FROM Users INNER JOIN User_Auth ON (Users.UUID = User_Auth.UUID) WHERE (Users.username = _username AND User_Auth.password = _password);
	IF records = 1 THEN
		RETURN true;
	ELSE
		RETURN false;
	END IF;
end $$ LANGUAGE plpgsql;


CREATE OR replace FUNCTION Change_Password (_username VARCHAR, _password VARCHAR, _salt VARCHAR)
RETURNS boolean AS $$
declare 
    usr_UUID CHAR(16);
    num_Auth_records INTEGER;
begin
    SELECT Users.UUID INTO usr_UUID FROM Users WHERE (username = _username);
    SELECT COUNT(*) INTO num_Auth_records FROM User_Auth WHERE (username = _username);
    IF num_Auth_records = 0 THEN
        INSERT INTO User_Auth VALUES (usr_UUID, _password, _salt);
    ELSE
        UPDATE User_Auth SET password=_password, salt=_salt WHERE (UUID=usr_UUID);
    END IF;
end $$ LANGUAGE plpgsql;





''')
