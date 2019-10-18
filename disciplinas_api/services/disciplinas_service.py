from infra.disciplinas_dao import \
    listar as dao_listar, \
    consultar as dao_consultar, \
    consultar_por_nome as dao_consultar_por_nome, \
    cadastrar as dao_cadastrar, \
    alterar as dao_alterar, \
    remover as dao_remover, \
    cadastrar_aluno as dao_cadastrar_aluno, \
    remover_aluno as dao_remover_aluno, \
    consultar_alunos as dao_consultar_alunos

from model.disciplina import Disciplina

def listar():
    return [disciplina.__dict__() for disciplina in dao_listar()]

def localizar_disciplina(id):
    return dao_consultar(id)

def localizar(id):
    disciplina = localizar_disciplina(id)
    return disciplina.__dict__() if disciplina != None else None

def localizar_por_nome(nome):
    disciplina = dao_consultar_por_nome(nome)
    return disciplina.__dict__() if disciplina != None else None

def criar(dados):
    if localizar_por_nome(dados['nome']) == None:
        disciplina = Disciplina.criar(dados)
        return dao_cadastrar(disciplina).__dict__()
    return None

def remover(id):
    disciplina = localizar_disciplina(id)
    if disciplina == None:
        return False
    return dao_remover(disciplina)

def atualizar(dados):
    if localizar(dados['id']) != None:
        disciplina = Disciplina.criar(dados)
        dao_alterar(disciplina)
        return localizar(disciplina.id)
    return None
    
def resetar():
    disciplinas = listar()
    for disciplina in disciplinas:
        dao_remover(disciplina)
