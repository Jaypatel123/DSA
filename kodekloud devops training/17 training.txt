
a. Create a database user kodekloud_top and set its password to TmPcZjtRQx. 
b. Create a database kodekloud_db10 and grant full permissions to user kodekloud_top on this database.


######## Solution #########
vvvvvvvvvvvvvvvvvvvvvvvvv

sudo -i -u postgres

psql

CREATE USER kodekloud_top WITH PASSWORD 'TmPcZjtRQx';

## check database user creation using \du

CREATE DATABASE kodekloud_db10;

## check database creation using \l

GRANT ALL PRIVILEGES ON DATABASE kodekloud_db10 TO kodekloud_top;

## check attached permissions to database \l

