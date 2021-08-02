import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect('database.db')

def insertUser(email,username,password): # inser usuário no BD
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    password = generate_password_hash(password, method='sha256')
    cur.execute("INSERT INTO users (email,username,senha) VALUES (?,?,?)", (email,username,password))
    con.commit()
    con.close()

with open('schema.sql') as f:
    connection.executescript(f.read())
    insertUser('theresa.mancini@hotmail.com','Theresa','123456')
    insertUser('joana123@hotmail.com','Joana','987654')
    insertUser('abc@hotmail.com','João','abc123')




                                


connection.commit()
connection.close()