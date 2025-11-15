from db import initdb
from aluno import Aluno
from alunoservice import AlunoService

if __name__ == "__main__":
    initdb()
    aluno1 = Aluno(20230262, "Caio", "30/10/2004")
    aluno2 = Aluno(20230261, "Caio", "30/10/2004")
    aluno3 = Aluno(20230264, "Caio", "30/10/2004")
    service = AlunoService()
    service.salvar(aluno1)
    service.salvar(aluno2)
    service.salvar(aluno3)
    alunos = service.listar_aluno()

    print(alunos)
    