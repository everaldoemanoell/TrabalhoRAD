class Disciplina:
    id = None
    nome = None
    turno = None
    sala = None
    professor = None
    
    def __init__ (self, id, nome, turno, sala, professor):
        self.id = id
        self.nome = nome
        self.turno = turno
        self.sala = sala
        self.professor = professor 