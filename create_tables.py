#!/bin/python3

import psycopg2
import configparser

config = configparser.RawConfigParser()
config.read('conf.ini')

dbname = config.get('DatabaseSection', 'database.dbname')
dbuser = config.get('DatabaseSection', 'database.user')

db = psycopg2.connect("dbname=" + dbname + " user=" + dbuser)

cur = db.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS hdfcoll(
  idcoll INTEGER,
  idfilms INTEGER,
  PRIMARY KEY(idcoll, idfilms)
);

CREATE TABLE IF NOT EXISTS hdffilms(
  idfilms	integer,
  titre	VARCHAR(150),
  annee	INTEGER,
  type	INTEGER,
  PRIMARY KEY(idfilms)
);

CREATE TABLE hdftypelabel(
  type	INTEGER NOT NULL,
  label	VARCHAR(20),
  PRIMARY KEY(type)
);

CREATE TABLE IF NOT EXISTS acnat(
  idnat	INTEGER UNIQUE,
  libel	VARCHAR(30),
  idcoll INTEGER,
  PRIMARY KEY(idnat)
);

CREATE TABLE accoll(
  idcoll	INTEGER,
  idfilms	INTEGER,
  PRIMARY KEY(idcoll,idfilms)
);

CREATE TABLE IF NOT EXISTS wplabel(
id	TEXT UNIQUE,
label	TEXT,
PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS acfilms(
  idfilms	TEXT,
  titre	NUMERIC,
  titreo	TEXT,
  annee	INTEGER,
  duree	INTEGER,
  real	TEXT,
  acteur TEXT,
  nationalite TEXT,
  note	TEXT,
  PRIMARY KEY(idfilms)
);
CREATE TABLE imdbfilms(
  idfilms	TEXT UNIQUE,
  titre	TEXT,
  annee	INTEGER,
  note	TEXT,
  PRIMARY KEY(idfilms)
);
CREATE TABLE IF NOT EXISTS scliste(
  idliste	TEXT,
  idfilms	INTEGER,
  numero	INTEGER,
  PRIMARY KEY(idliste,idfilms,numero)
);
CREATE TABLE IF NOT EXISTS trfilms(
  idhdf	INTEGER,
  idsc	INTEGER,
  idac	TEXT,
  idimdb	TEXT,
  idwd	TEXT,
  PRIMARY KEY(idhdf,idimdb,idsc)
);
CREATE TABLE IF NOT EXISTS wdfilms(
  idfilms	TEXT UNIQUE,
  idac	TEXT,
  idimdb	TEXT,
  urlwp	TEXT,
  PRIMARY KEY(idfilms)
);
CREATE TABLE IF NOT EXISTS wdliste(
  idliste	TEXT,
  idwd	TEXT,
  idimdb	TEXT,
  PRIMARY KEY(idliste,idwd)
);
CREATE TABLE IF NOT EXISTS scfilms(
  idfilms	INTEGER UNIQUE,
  titre	VARCHAR(150),
  annee	INTEGER,
  url	VARCHAR(300),
  note	TEXT,
  idimdb	TEXT,
  PRIMARY KEY(idfilms)
);
CREATE TABLE ptpcoll(
  idcoll	INTEGER,
  idfilms	INTEGER,
  idimdb	TEXT,
  PRIMARY KEY(idcoll,idfilms)
);
CREATE TABLE IF NOT EXISTS br(
  id	TEXT,
  titre	TEXT,
  date	TEXT,
  url	TEXT,
  idimdb	TEXT
);
CREATE TABLE IF NOT EXISTS trcoll(
  idhdf	INTEGER,
  idsc	TEXT,
  idac	INTEGER,
  idwd	TEXT,
  idptp	INTEGER,
  titre	TEXT,
  url	TEXT,
  tri	INTEGER,
  manquant	INTEGER,
  PRIMARY KEY(idhdf,idsc,idwd)
);
CREATE TABLE IF NOT EXISTS telefilms(
  idfilms	INTEGER UNIQUE,
  titre	TEXT,
  annee	INTEGER,
  real	TEXT,
  note	TEXT,
  note_img	TEXT,
  url	TEXT,
  idac	INTEGER,
  PRIMARY KEY(idfilms)
);
/* No STAT tables available */
        """)

cur.close()
db.commit()
db.close()

