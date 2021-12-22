
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), account VARCHAR (32), status VARCHAR (16));
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS location;
CREATE TABLE location (id_product INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32) UNIQUE, direction INTEGER NOT NULL, price INTEGER, status iNTEGER);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS direction;
CREATE TABLE direction (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, public_name VARCHAR (32) UNIQUE);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS locations;
CREATE TABLE locations (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32) UNIQUE, direction_id INTEGER NOT NULL, price INTEGER, status iNTEGER, FOREIGN KEY (direction_id) REFERENCES direction (id));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;