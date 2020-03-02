role creation commands
------------------------------
CREATE ROLE lowPerm WITH LOGIN PASSWORD 'dca3729609c9c7b649bb';


logging in commands
------------------------------
psql -U [username] database	#log into database as user
\password [username]		#change password for user


information gathering commands
------------------------------
\conninfo			#gets who's logged in, on what database etc
\dt				#gets current relations/schemas
SELECT * FROM pg_roles;		#gets roles and permissions
\du+				# "
select * from pg_shadow;	#gets roles' passwords





INSERT INTO users VALUES ('14henderson', 'a', 'a', 'a', 'Niklas', 'Henderson', '1998-06-06');








su apiUser
psql


user: lowPerm
get roles: SELECT * FROM pg_roles;
\du+ to get roles and attributes


CREATE ROLE lowPerm WITH LOGIN PASSWORD 'dca3729609c9c7b649bb';
psql -U lowPerm -W postgres;

/etc/postgresql/10/main/pg_hba.conf
service postgresql restart


select * from pg_shadow;
\password lowPerm;




abc123: md523d0c931e69c66225b911df037f4b6f1

\conninfo
\dt
psql -U lowperm apiUser
psql


lowperm
role creation commands
------------------------------
CREATE ROLE lowPerm WITH LOGIN PASSWORD 'dca3729609c9c7b649bb';


logging in commands
------------------------------
psql -U lowperm apiUser


information gathering commands
------------------------------
\conninfo			#gets who's logged in, on what database etc
\dt				#gets current relations/schemas
SELECT * FROM pg_roles;		#gets roles and permissions
\du+				# "
select * from pg_shadow;	#gets roles' passwords
