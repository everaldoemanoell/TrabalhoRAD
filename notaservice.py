from db import get_conexao
from nota import Nota

class NotaService:
    def salvar(self, nota):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO notas(valor, matricula, disciplina_id) 
            VALUES (?, ?, ?)
        """,(nota.valor, nota.matricula, nota.disciplina_id))
        con.commit()
        con.close()
        return nota

    def listar_disciplina(self):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            SELECT valor, matricula, disciplina_id FROM notas
        """)
        resultados = cursor.fetchall()
        con.close()
        
        return [
            Nota(resultado[0], resultado[1], resultado[2]) for resultado in resultados
        ]

    def editar(self, nota):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE notas SET valor = ?, matricula = ?, disciplina_id = ? WHERE matricula = ? AND disciplina_id = ?
        """,(nota.valor, nota.matricula, nota.disciplina_id, nota.matricula, nota.disciplina_id))
        con.commit()
        con.close()

        return nota

    def excluir(self, nota):
        con = get_conexao()
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM notas WHERE matricula = ? AND disciplina_id = ?
        """,(nota.matricula, nota.disciplina_id))
        con.commit()
        con.close()
    