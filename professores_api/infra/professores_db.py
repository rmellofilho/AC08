import sqlite3

db_name = "professores.db"
table_name = "professor"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, nome text NOT NULL UNIQUE, rg text NOT NULL UNIQUE);"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, nome, rg):
    sql = f"INSERT INTO {table_name} (nome, rg) VALUES (?, ?)"
    cursor.execute(sql, (nome, rg))

def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, "Tiago Alexandre", "12345678-1")
        popularDb(cursor, "Lucas Mendes", "12345678-2")
        popularDb(cursor, "Victor Williams", "12345678-3")
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()