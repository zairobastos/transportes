import sqlite3
from contextlib import closing

def create_database():
    try:
        with closing(sqlite3.connect('./database/database.db')) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transporte (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        linha INT,
                        data_inicio TEXT,
                        data_fim TEXT,
                        horas INTEGER,
                        modelo TEXT,
                        temperatura REAL,
                        candidatos INTEGER,
                        prompt TEXT,
                        valores_exatos TEXT,
                        valores_previstos TEXT,
                        smape REAL,
                        tempo REAL,
                        tokens INTEGER
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mercado (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        produto TEXT,
                        data_inicio TEXT,
                        data_fim TEXT,
                        dias INTEGER,
                        modelo TEXT,
                        temperatura REAL,
                        candidatos INTEGER,
                        prompt TEXT,
                        valores_exatos TEXT,
                        valores_previstos TEXT,
                        smape REAL,
                        tempo REAL,
                        tokens INTEGER
                    );
                """)
                connection.commit() 
            print("Conexão com o banco de dados estabelecida e tabelas criadas com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados ou criar tabelas: {e}")

if __name__ == "__main__":
    create_database()
    