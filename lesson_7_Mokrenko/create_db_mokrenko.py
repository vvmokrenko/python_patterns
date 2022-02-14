import sqlite3

con = sqlite3.connect('db_mokrenko.sqlite')
cur = con.cursor()
with open('create_db_mokrenko.sql', 'r', encoding='UTF-8') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
