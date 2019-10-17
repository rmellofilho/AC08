# Exceção lançada quando se tenta associar um ID a uma entidade que já possui um.
class NaoTransienteException(Exception):
    pass

class AlunoJaInclusoException(Exception):
    pass

class Disciplina():
    
    def __init__(self, nome, professor_id):
        self.id = None
        self.nome = nome
        self.professor_id = professor_id
        self.alunos = []
    
    def associar_id(self, id):
        pass
    
    def incluir_aluno(self, aluno_id):
        pass
    
    def associar_alunos(self, alunos):
        pass
    
    def remover_aluno(self, aluno_id):
        pass
    
    def verificar_transiente(self):
        pass
    
    def validar(self):
        pass
    
    def atualizar(self, dados):
        pass

    def __dict__(self):
        pass

    @staticmethod
    def criar(dados):
        pass
    
    @staticmethod    
    def criar_com_id(id, nome, professor_id):
        pass