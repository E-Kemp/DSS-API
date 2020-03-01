/*For lowperm. SELECT commands only, on non-sensitive relations*/
CREATE ROLE lowPerm WITH LOGIN PASSWORD 'dca3729609c9c7b649bb';
REVOKE CREATE ON SCHEMA public FROM lowperm;
GRANT SELECT ON Users TO lowperm;
GRANT SELECT ON Posts TO lowperm;
GRANT SELECT ON Comments TO lowperm;


/*For insertperm. SELECT, INSERT, DELETE and UPDATE commands only, on non-sensitive relations*/
CREATE ROLE insertperm WITH LOGIN PASSWORD 'cc663ef4d05c7055cba9';
REVOKE CREATE ON SCHEMA public FROM insertperm;
GRANT SELECT ON Users TO insertperm;
GRANT INSERT ON Users TO insertperm;
GRANT DELETE ON Users TO insertperm;
GRANT UPDATE ON Users TO insertperm;

GRANT SELECT ON Posts TO insertperm;
GRANT INSERT ON Posts TO insertperm;
GRANT DELETE ON Posts TO insertperm;
GRANT UPDATE ON Posts TO insertperm;

GRANT SELECT ON Comments TO insertperm;
GRANT INSERT ON Comments TO insertperm;
GRANT DELETE ON Comments TO insertperm;
GRANT UPDATE ON Comments TO insertperm;




/*For authperm. SELECT, INSERT, DELETE and UPDATE commands only, on non-sensitive relations*/
CREATE ROLE authperm WITH LOGIN PASSWORD 'eb6afa7b272eb7ffd531';
REVOKE CREATE ON SCHEMA public FROM authperm;
GRANT SELECT ON Users TO authperm;


GRANT SELECT ON User_Auth TO authperm;
GRANT INSERT ON User_Auth TO authperm;