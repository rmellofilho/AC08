# Exceção lançada quando se tenta associar um ID a uma entidade que já possui um.
class NaoTransienteException(Exception):
    pass

class Aluno():
    
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.id = None
    
    def associar_id(self, id):
        if self.id != None:
            raise NaoTransienteException
        self.id = id
    
    def verificar_transiente(self):
        if self.id != None:
            return False
        return True
    
    def validar(self):
        if self.nome != None and self.matricula != None:
            return True
        return False
    
    def atualizar(self, dados):
        try:
            nome = dados["nome"]
            matricula = dados["matricula"]
            self.nome, self.matricula = nome, matricula
            return self
        except Exception as e:
            print("Problema ao atualizar!")
            print(e)

    def __dict__(self):
        d = dict()
        d['id'] = self.id
        d['nome'] = self.nome
        d['matricula'] = self.matricula
        return d

    @staticmethod
    def criar(dados):
        try:
            nome = dados["nome"]
            matricula = dados["matricula"]
            return Aluno(nome=nome, matricula=matricula)
        except Exception as e:
            print("Problema ao criar novo aluno!")
            print(e)
    
    @staticmethod    
    def criar_com_id(id, nome, matricula):
        try:
            aluno = Aluno(nome=nome, matricula=matricula)
            aluno.associar_id(id)
            return aluno
        except Exception as e:
            print("Problema ao criar novo aluno!")
            print(e)