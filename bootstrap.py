import sqlite3
import config

qry = open('bootstrap.sql', 'r').read()
conn = sqlite3.connect(config.DATABASE_LOC)
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
