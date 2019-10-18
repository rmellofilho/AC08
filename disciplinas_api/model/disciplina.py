'''
 Exceção lançada quando se tenta associar um ID a
 uma entidade que já possui um.
'''


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
        if self.id is None:
            raise NaoTransienteException
        self.id = id

    def incluir_aluno(self, aluno_id):
        self.aluno_id = aluno_id

    def associar_alunos(self, alunos):
        pass

    def remover_aluno(self, aluno_id):
        pass

    def verificar_transiente(self):
        if self.id is None:
            return False
        return True

    def validar(self):
        if self.id is None and self.nome is None
        and self.professor_id is None and self.alunos is None:
            return True
        return False

    def atualizar(self, dados):
        try:
            nome = dados["nome"]
            professor_id = dados["professor_id"]
            alunos = dados["alunos"]
            self.nome, self.professor_id, self.alunos =
            nome, professor_id, alunos
            return self
        except Exception as e:
            print("Problema ao atualizar!")
            print(e)

    def __dict__(self):
        d = dict()
        d['id'] = self.id
        d['nome'] = self.nome
        d['professor_id'] = self.professor_id
        d['alunos'] = self.alunos
        return d

    @staticmethod
    def criar(dados):
        try:
            nome = dados["nome"]
            professor_id = dados["professor_id"]
            alunos = dados["alunos"]
            return Aluno(nome=nome, professor_id=professor_id)
        except Exception as e:
            print("Problema ao criar novo aluno!")
            print(e)

    @staticmethod
    def criar_com_id(id, nome, professor_id):
        pass
