import sqlite3

def get_conexao():
    return sqlite3.connect("banco.db")

def initdb():
    con = get_conexao()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos(
            matricula INTEGER PRIMARY KEY,
            nome VARCHAR NOT NULL,
            dt_nascimento VARCHAR NOT NULL
        )
    """)
    con.commit()
    con.close()