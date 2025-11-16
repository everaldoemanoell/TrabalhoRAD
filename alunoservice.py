from db import get_conexao
from aluno import Aluno

class AlunoService:
    def salvar(self, aluno):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO alunos(matricula, nome, dt_nascimento) 
            VALUES (?, ?, ?)
        """,(aluno.matricula, aluno.nome, aluno.dt_nascimento))
        con.commit()
        con.close()
        return aluno

    def listar_aluno(self):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            SELECT matricula, nome, dt_nascimento FROM alunos  
        """)
        resultados = cursor.fetchall()
        con.close()
        
        return [
            Aluno(resultado[0], resultado[1], resultado[2]) for resultado in resultados
        ]

    def editar(self, aluno):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE alunos SET nome = ?, dt_nascimento = ? WHERE matricula = ?
        """,(aluno.nome, aluno.dt_nascimento, aluno.matricula))
        con.commit()
        con.close()

        return aluno

    def excluir(self, matricula):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM alunos WHERE matricula = ?
        """,(matricula))
        con.commit()
        con.close()
    