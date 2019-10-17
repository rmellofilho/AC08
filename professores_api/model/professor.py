# Exceção lançada quando se tenta associar um ID a uma entidade que já possui um.
class NaoTransienteException(Exception):
    pass

class Professor():
    
    def __init__(self, nome, rg):
        self.nome = nome
        self.rg = rg
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
        if self.nome != None and self.rg != None:
            return True
        return False
    
    def atualizar(self, dados):
        try:
            nome = dados["nome"]
            rg = dados["rg"]
            self.nome, self.rg = nome, rg
            return self
        except Exception as e:
            print("Problema ao atualizar!")
            print(e)

    def __dict__(self):
        d = dict()
        d['id'] = self.id
        d['nome'] = self.nome
        d['rg'] = self.rg
        return d

    @staticmethod
    def criar(dados):
        try:
            nome = dados["nome"]
            rg = dados["rg"]
            return Professor(nome=nome, rg=rg)
        except Exception as e:
            print("Problema ao criar novo professor!")
            print(e)
    
    @staticmethod    
    def criar_com_id(id, nome, rg):
        try:
            professor = Professor(nome=nome, rg=rg)
            professor.associar_id(id)
            return professor
        except Exception as e:
            print("Problema ao criar novo professor!")
            print(e)