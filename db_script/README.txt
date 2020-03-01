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




information gathering commands
------------------------------
\conninfo			#gets who's logged in, on what database etc
\dt				#gets current relations/schemas
SELECT * FROM pg_roles;		#gets roles and permissions
