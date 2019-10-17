import sqlite3
from model.disciplina import Disciplina
from contextlib import closing

db_name = "disciplinas.db"
model_name = "disciplina"
model_name_relationship = "disciplina_aluno"

def con():
    return sqlite3.connect(db_name)

def listar():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, professor_id FROM {model_name}")
        pass

def consultar(id):
    pass

def consultar_por_nome(nome):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, professor_id FROM {model_name} WHERE nome = ?", (nome,))
        pass

def cadastrar(disciplina):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name} (nome, professor_id) VALUES (?, ?)"
        result = cursor.execute(sql, (disciplina.nome, disciplina.professor_id))
        connection.commit()
        if cursor.lastrowid:
            disciplina.associar_id(cursor.lastrowid)
            return disciplina
        else:
            return None

def alterar(disciplina):
    pass

def remover(disciplina):
    pass

#Disciplina-aluno

def cadastrar_aluno(disciplina, aluno_id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name_relationship} (disciplina_id, aluno_id) VALUES (?, ?)"
        result = cursor.execute(sql, (disciplina.id, aluno_id))
        pass
            
def remover_aluno(disciplina, aluno_id):
    pass
    
def consultar_alunos(disciplina):
    pass
    