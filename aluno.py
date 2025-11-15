class Aluno:
    matricula = 0
    nome = ""
    dt_nascimento = ""
    
    def __init__ (self, matricula, nome, dt_nascimento):
        self.matricula = matricula
        self.nome = nome
        self.dt_nascimento = dt_nascimento