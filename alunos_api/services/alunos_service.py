from infra.alunos_dao import \
    listar as dao_listar, \
    consultar as dao_consultar, \
    consultar_por_nome as dao_consultar_por_nome, \
    cadastrar as dao_cadastrar, \
    alterar as dao_alterar, \
    remover as dao_remover

from model.aluno import Aluno

def listar():
    return [aluno.__dict__() for aluno in dao_listar()]

def localizar_aluno(id):
    return dao_consultar(id)

def localizar(id):
    aluno = localizar_aluno(id)
    return aluno.__dict__() if aluno != None else None
    
def localizar_por_nome(nome):
    aluno = dao_consultar_por_nome(nome)
    return aluno.__dict__() if aluno != None else None

def criar(aluno_data):
    if localizar_por_nome(aluno_data['nome']) == None:
        aluno = Aluno.criar(aluno_data)
        return dao_cadastrar(aluno).__dict__()
    return None

def remover(id):
    aluno = localizar_aluno(id)
    if aluno == None:
        return False
    return dao_remover(aluno)

def atualizar(aluno_data):
    if localizar_por_nome(aluno_data['nome']) != None:
        aluno = Aluno.criar(aluno_data)
        dao_alterar(aluno)
        return localizar(aluno.id)
    return None
    
def resetar():
    alunos = listar()
    for aluno in alunos:
        dao_remover(aluno)