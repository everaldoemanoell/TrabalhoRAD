import sqlite3

def get_conexao():
    con = sqlite3.connect("banco.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR NOT NULL,
            turno VARCHAR NOT NULL,
            sala VARCHAR NOT NULL,
            professor VARCHAR NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas(
            matricula VARCHAR NOT NULL,
            valor REAL NOT NULL,
            disciplina_id INTEGER NOT NULL,
            PRIMARY KEY(matricula, disciplina_id),
            FOREIGN KEY(matricula) REFERENCES alunos(matricula),
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
        )
    """)
    con.commit()
    con.close()

