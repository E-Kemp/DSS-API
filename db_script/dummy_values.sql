BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Comments" (
	"UUID"	VARCHAR(10) NOT NULL,
	"body"	TEXT NOT NULL,
	"date_posted"	DATE NOT NULL,
	"time_posted"	TIME NOT NULL,
	"user_UUID"	CHAR(16) NOT NULL,
	"post_UUID"	VARCHAR(10) NOT NULL,
	PRIMARY KEY("UUID"),
	FOREIGN KEY("user_UUID") REFERENCES "Users"("UUID"),
	FOREIGN KEY("post_UUID") REFERENCES "Posts"("UUID")
);
CREATE TABLE IF NOT EXISTS "Posts" (
	"UUID"	VARCHAR(10) NOT NULL,
	"heading"	VARCHAR(512) NOT NULL,
	"body"	TEXT,
	"date_posted"	DATE NOT NULL,
	"time_posted"	TIME NOT NULL,
	"user_UUID"	CHAR(16) NOT NULL,
	PRIMARY KEY("UUID"),
	FOREIGN KEY("user_UUID") REFERENCES "Users"("UUID")
);
CREATE TABLE IF NOT EXISTS "User_Auth" (
	"UUID"	CHAR(16) NOT NULL UNIQUE,
	"password"	VARCHAR(255) NOT NULL,
	"salt"	VARCHAR(255) NOT NULL,
	PRIMARY KEY("UUID"),
	FOREIGN KEY("UUID") REFERENCES "Users"("UUID")
);
CREATE TABLE IF NOT EXISTS "Users" (
	"UUID"	CHAR(16) NOT NULL UNIQUE,
	"username"	VARCHAR(255) NOT NULL UNIQUE,
	"email"	VARCHAR(255) NOT NULL,
	"forename"	VARCHAR(255) NOT NULL,
	"surname"	VARCHAR(255) NOT NULL,
	"DOB"	DATE NOT NULL,
	PRIMARY KEY("UUID")
);
INSERT INTO "Posts" ("UUID","heading","body","date_posted","time_posted","user_UUID") VALUES ('f34bf76efc738bb677a0','Favourite films?','My name is geoff and this is my first post!
Question: what is your favourite film?','2020-03-06','00:10:49','01705773f94e8329c1b8dca9cbdef482');
INSERT INTO "User_Auth" ("UUID","password","salt") VALUES ('6cca12861959a8aaa36433b35b9c39a9','fc06b24423e8c59298cfb63fcaad6ab93b90707a1402226e7feae89fad3eb2ec','d2586b09e16d2358b44cad530d837d4804ad6154');
INSERT INTO "User_Auth" ("UUID","password","salt") VALUES ('01705773f94e8329c1b8dca9cbdef482','47ca13a8a08ae38679f411ba7b88add05ef32b4f29dd0649c6c9c948d0435197','a412e5499f67a37d22c71aa7430ff0e5f67e432b');
INSERT INTO "User_Auth" ("UUID","password","salt") VALUES ('829af3197ff6878345b69e59baec3bca','d333913b9b06c23f5b44ddcafdfe41abf9c204744b87f72d36b22ca495eebbdd','19c3bc80cb2697a46a88e1d37aaab3bebaa50484');
INSERT INTO "User_Auth" ("UUID","password","salt") VALUES ('efbdf3407819e24840379c0441d1ea6b','bb6ebaa0a521e99f31acc122a73112bf778b83353e7249dbaff8bf9522df6918','3aeb16530e9ab0eca853e896534dc07455a2c05d');
INSERT INTO "User_Auth" ("UUID","password","salt") VALUES ('00dfd256219d54a1f71bf3ddae45f6d3','c34348af239cde989e1d383d7cf0bbe8fc6324cee79215b5c93f529ecae9850a','c6f41adf4cef5d74d3902ab5885a0bf26885039c');
INSERT INTO "Users" ("UUID","username","email","forename","surname","DOB") VALUES ('6cca12861959a8aaa36433b35b9c39a9','14henderson','niklas.henderson@btinternet.com','Niklas','Henderson','1998-06-06');
INSERT INTO "Users" ("UUID","username","email","forename","surname","DOB") VALUES ('01705773f94e8329c1b8dca9cbdef482','Geoff123','G.daniels@gmail.com','Geoff','Daniels','1993-03-06');
INSERT INTO "Users" ("UUID","username","email","forename","surname","DOB") VALUES ('829af3197ff6878345b69e59baec3bca','Abba_lover123','a.b@gmail.com','Kate','Davies','2001-02-05');
INSERT INTO "Users" ("UUID","username","email","forename","surname","DOB") VALUES ('efbdf3407819e24840379c0441d1ea6b','Cake_eater','Lucy.preston@hotmail.com','Lucy','Preston','1997-02-05');
INSERT INTO "Users" ("UUID","username","email","forename","surname","DOB") VALUES ('00dfd256219d54a1f71bf3ddae45f6d3','princess_87623','p.wee@bw.co.uk','Shack','Big','1997-05-30');
COMMIT;
