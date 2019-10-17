import sqlite3

db_name = "alunos.db"
table_name = "aluno"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, nome text NOT NULL UNIQUE, matricula integer NOT NULL UNIQUE);"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, nome, matricula):
    sql = f"INSERT INTO {table_name} (nome, matricula) VALUES (?, ?)"
    cursor.execute(sql, (nome, matricula))

def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, "Thomas Alexandre", 12345)
        popularDb(cursor, "Lucio Mendes", 12346)
        popularDb(cursor, "Vinicius Williams", 12347)
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()