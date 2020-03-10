import sqlite3

db = sqlite3.connect('../database.db')
cur = db.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS User_Auth;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;


CREATE TABLE Users(
    UUID VARCHAR(40) PRIMARY KEY NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    forename VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL
);

CREATE TABLE User_Auth(
    UUID VARCHAR(40) PRIMARY KEY NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    verification_code VARCHAR(255) NOT NULL UNIQUE,
    FOREIGN KEY (UUID) REFERENCES Users(UUID)
);


CREATE TABLE Posts(
    UUID VARCHAR(40) PRIMARY KEY NOT NULL,
    heading VARCHAR(512) NOT NULL,
    body TEXT,
    date_posted DATE NOT NULL,
    time_posted TIME NOT NULL,
    user_UUID VARCHAR(40) NOT NULL,
    FOREIGN KEY (user_UUID) REFERENCES Users(UUID)
);

CREATE TABLE Comments(
    UUID VARCHAR(40) PRIMARY KEY NOT NULL,
    body TEXT NOT NULL,
    date_posted DATE NOT NULL,
    time_posted TIME NOT NULL,
    user_UUID VARCHAR(40) NOT NULL,
    post_UUID VARCHAR(40) NOT NULL,
    FOREIGN KEY (user_UUID) REFERENCES Users(UUID),
    FOREIGN KEY (post_UUID) REFERENCES Posts(UUID)
);

CREATE TABLE Sessions(
	UUID VARCHAR(40) PRIMARY KEY NOT NULL,
	ip VARCHAR(15),
	csrf VARCHAR(40)
	);

''')

#SELECT COUNT(Users.UUID) INTO records FROM Users INNER JOIN User_Auth ON (Users.UUID = User_Auth.UUID) WHERE (User_Auth.verified = 'TRUE');


# CREATE OR replace FUNCTION Authenticate_User (_username VARCHAR, _password VARCHAR)
# RETURNS boolean AS $$
# declare
    # records INTEGER;
# begin
    # SELECT COUNT(Users.UUID) INTO records FROM Users INNER JOIN User_Auth ON (Users.UUID = User_Auth.UUID) WHERE (Users.username = _username AND User_Auth.password = _password AND User_Auth.verified = 'TRUE');
	# IF records = 1 THEN
		# RETURN true;
	# ELSE
		# RETURN false;
	# END IF;
# end $$ LANGUAGE plpgsql;


# CREATE OR replace FUNCTION Change_Password (_username VARCHAR, _password VARCHAR, _salt VARCHAR, _vericode VARCHAR)
# RETURNS void AS $$
# declare 
    # usr_UUID VARCHAR(40);
    # num_Auth_records INTEGER;
# begin
    # SELECT Users.UUID INTO usr_UUID FROM Users WHERE (username = _username);
    # SELECT COUNT(*) INTO num_Auth_records FROM User_Auth WHERE (UUID = usr_UUID);
    # IF num_Auth_records = 0 THEN
        # INSERT INTO User_Auth VALUES (usr_UUID, _password, _salt, 'FALSE', _vericode);
    # ELSE
        # UPDATE User_Auth SET password=_password, salt=_salt, verification_code=_vericode WHERE (UUID=usr_UUID);
    # END IF;
# end $$ LANGUAGE plpgsql;





