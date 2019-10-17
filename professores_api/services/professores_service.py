from infra.professores_dao import \
    listar as dao_listar, \
    consultar as dao_consultar, \
    consultar_por_nome as dao_consultar_por_nome, \
    cadastrar as dao_cadastrar, \
    alterar as dao_alterar, \
    remover as dao_remover

from model.professor import Professor

def listar():
    return [professor.__dict__() for professor in dao_listar()]

def localizar_professor(id):
    return dao_consultar(id)

def localizar(id):
    professor = localizar_professor(id)
    return professor.__dict__() if professor != None else None
    
def localizar_por_nome(nome):
    professor = dao_consultar_por_nome(nome)
    return professor.__dict__() if professor != None else None

def criar(professor_data):
    if localizar_por_nome(professor_data['nome']) == None:
        professor = Professor.criar(professor_data)
        return dao_cadastrar(professor).__dict__()
    return None

def remover(id):
    professor = localizar_professor(id)
    if professor == None:
        return False
    return dao_remover(professor)

def atualizar(professor_data):
    if localizar_por_nome(professor_data['nome']) != None:
        professor = Professor.criar(professor_data)
        dao_alterar(professor)
        return localizar(professor.id)
    return None
    
def resetar():
    professores = listar()
    for professor in professores:
        dao_remover(professor)