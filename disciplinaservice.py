from db import get_conexao
from disciplina import Disciplina

class DisciplinaService:
    def salvar(self, disciplina):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO disciplinas(nome, turno, sala, professor) 
            VALUES (?, ?, ?, ?)
        """,(disciplina.nome, disciplina.turno, disciplina.sala, disciplina.professor))
        con.commit()
        con.close()
        return disciplina

    def listar_disciplina(self):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            SELECT id, nome, turno, sala, professor FROM disciplinas 
        """)
        resultados = cursor.fetchall()
        con.close()
        
        return [
            Disciplina(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4]) for resultado in resultados
        ]

    def editar(self, disciplina):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE disciplinas SET nome = ?, turno = ?, sala = ?, professor = ? WHERE id = ?
        """,(disciplina.nome, disciplina.turno, disciplina.sala, disciplina.professor, disciplina.id))
        con.commit()
        con.close()

        return disciplina

    def excluir(self, id):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM disciplinas WHERE id = ?
        """,(id))
        con.commit()
        con.close()
    