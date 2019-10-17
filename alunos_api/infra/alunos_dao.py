import sqlite3
from model.aluno import Aluno
from contextlib import closing

db_name = "alunos.db"
model_name = "aluno"

def con():
    return sqlite3.connect(db_name)

def listar():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, matricula FROM {model_name}")
        rows = cursor.fetchall()
        registros = []
        for (id, nome, matricula) in rows:
            aluno = Aluno.criar_com_id(id, nome, matricula)
            if aluno != None:
                registros.append(aluno)
        return registros

def consultar(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, matricula FROM {model_name} WHERE id = ?", (int(id),))
        row = cursor.fetchone()
        if row == None:
            return None
        return Aluno.criar_com_id(row[0],row[1],row[2])

def consultar_por_nome(nome):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, matricula FROM {model_name} WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row == None:
            return None
        return Aluno.criar_com_id(row[0],row[1],row[2])

def cadastrar(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name} (nome, matricula) VALUES (?, ?)"
        result = cursor.execute(sql, (aluno.nome, aluno.matricula))
        connection.commit()
        if cursor.lastrowid:
            aluno.associar_id(cursor.lastrowid)
            return aluno
        else:
            return None

def alterar(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"UPDATE {model_name} SET nome = ?, matricula = ? WHERE id = ?"
        cursor.execute(sql, (aluno.nome, aluno.matricula, aluno.id))
        connection.commit()
        if cursor.rowcount > 0:
            return True
        return False

def remover(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"DELETE FROM {model_name} WHERE id = ?"
        cursor.execute(sql, f"{aluno.id}")
        connection.commit()
        if cursor.rowcount > 0:
            return True
        return False