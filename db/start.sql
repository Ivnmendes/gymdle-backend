-- start.sql
CREATE ROLE gymdle_user WITH LOGIN PASSWORD '10012005';
CREATE DATABASE gymdle_db OWNER gymdle_user;
\c gymdle_db; 
GRANT ALL PRIVILEGES ON SCHEMA public TO gymdle_user;
ALTER ROLE gymdle_user SET client_encoding TO 'utf8';
ALTER ROLE gymdle_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gymdle_user SET timezone TO 'UTC';