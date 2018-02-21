-- Connect as privilged user

-- Create a tablespace for storing schema objects

CREATE TABLESPACE dbloadgen_ts
DATAFILE SIZE 2048M EXTENT MANAGEMENT LOCAL UNIFORM SIZE 4M;

-- Create user 

Create user dbloadgen identified by dbloadgen 
default tablespace dbloadgen_ts temporary tablespace temp;

Grant dba to dbloadgen;

prompt - Now connect as dbloadgen and create schema objects;

exit;

