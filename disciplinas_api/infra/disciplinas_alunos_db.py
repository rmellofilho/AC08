import sqlite3

db_name = "disciplinas.db"
table_name = "disciplina_aluno"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ...;"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, disciplina_id, aluno_id):
    pass

def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, 1, 1)
        popularDb(cursor, 2, 2)
        popularDb(cursor, 3, 3)
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()

