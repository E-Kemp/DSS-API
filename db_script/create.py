import sqlite3

db = sqlite3.connect('../database.db')
cur = db.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Comments;

CREATE TABLE Users(
    username VARCHAR(255) PRIMARY KEY NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    forename VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL
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




''')
