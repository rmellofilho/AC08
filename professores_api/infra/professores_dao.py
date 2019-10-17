import sqlite3
from model.professor import Professor
from contextlib import closing

db_name = "professores.db"
model_name = "professor"

def con():
    return sqlite3.connect(db_name)

def listar():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, rg FROM {model_name}")
        rows = cursor.fetchall()
        registros = []
        for (id, nome, rg) in rows:
            professor = Professor.criar_com_id(id, nome, rg)
            if professor != None:
                registros.append(professor)
        return registros

def consultar(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, rg FROM {model_name} WHERE id = ?", (int(id),))
        row = cursor.fetchone()
        if row == None:
            return None
        return Professor.criar_com_id(row[0],row[1],row[2])

def consultar_por_nome(nome):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT id, nome, rg FROM {model_name} WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row == None:
            return None
        return Professor.criar_com_id(row[0],row[1],row[2])

def cadastrar(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name} (nome, rg) VALUES (?, ?)"
        result = cursor.execute(sql, (professor.nome, professor.rg))
        connection.commit()
        if cursor.lastrowid:
            professor.associar_id(cursor.lastrowid)
            return professor
        else:
            return None

def alterar(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"UPDATE {model_name} SET nome = ?, rg = ? WHERE id = ?"
        cursor.execute(sql, (professor.nome, professor.rg, professor.id))
        connection.commit()
        if cursor.rowcount > 0:
            return True
        return False

def remover(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"DELETE FROM {model_name} WHERE id = ?"
        cursor.execute(sql, f"{professor.id}")
        connection.commit()
        if cursor.rowcount > 0:
            return True
        return False