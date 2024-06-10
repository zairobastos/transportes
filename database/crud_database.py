import sqlite3
import sqlite3
import json

class Crud:
    def __init__(self):
        self.connection = sqlite3.connect('./database/database.db')
        self.cursor = self.connection.cursor()

    def insert(self, **kwargs):
        if kwargs.get("table") == "transporte":
            try:
                valores_para_inserir = (
                    kwargs.get("linha"),
                    kwargs.get("data_inicio"),
                    kwargs.get("data_fim"),
                    kwargs.get("horas"),
                    kwargs.get("modelo"),
                    kwargs.get("temperatura"),
                    kwargs.get("candidatos"),
                    kwargs.get("prompt"),
                    kwargs.get("valores_exatos"),
                    kwargs.get("valores_previstos"),
                    kwargs.get("smape"),
                    kwargs.get("tempo"),
                    kwargs.get("tokens")
                )
                
                self.cursor.execute("""
                INSERT INTO transporte (linha, data_inicio, data_fim, horas, modelo, temperatura, candidatos, prompt, valores_exatos, valores_previstos, smape, tempo, tokens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", valores_para_inserir)
                self.connection.commit()
                print("Dados inseridos com sucesso!")
                return True
            except sqlite3.Error as e:
                print(f"Erro ao inserir dados na tabela transporte: {e}")
                return False
        elif kwargs.get("table") == "mercado":
            try:                
                valores_para_inserir = (
                    kwargs.get("produto"),
                    kwargs.get("data_inicio"),
                    kwargs.get("data_fim"),
                    kwargs.get("dias"),
                    kwargs.get("modelo"),
                    kwargs.get("temperatura"),
                    kwargs.get("candidatos"),
                    kwargs.get("prompt"),
                    kwargs.get("valores_exatos"),
                    kwargs.get("valores_previstos"),
                    kwargs.get("smape"),
                    kwargs.get("tempo"),
                    kwargs.get("tokens")
                )
                
                self.cursor.execute("""
                INSERT INTO mercado (produto, data_inicio, data_fim, dias, modelo, temperatura, candidatos, prompt, valores_exatos, valores_previstos, smape, tempo, tokens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", valores_para_inserir)
                self.connection.commit()
                print("Dados inseridos com sucesso!")
                return True
            except sqlite3.Error as e:
                print(f"Erro ao inserir dados na tabela mercado: {e}")
                return False
        else:
            print("Tabela não encontrada!")



    def select(self, **kwargs):
        if kwargs.get("table") == "transporte":
            try:
                self.cursor.execute("SELECT * FROM transporte")
                return self.cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Erro ao selecionar dados da tabela transporte: {e}")
        elif kwargs.get("table") == "mercado":
            try:
                self.cursor.execute("SELECT * FROM mercado")
                return self.cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Erro ao selecionar dados da tabela mercado: {e}")
        else:
            print("Tabela não encontrada!")

    def select_where(self, **kwargs):
        if kwargs.get("table") not in ("transporte", "mercado"):
            print("Tabela não encontrada!")
            return

        # Construir a string da consulta WHERE dinamicamente
        where_clauses = []
        for column, value in kwargs.items():
            if column in ("table", "limit", "offset"):
                continue  # Ignorar colunas reservadas

            if isinstance(value, str):
                value = f"'{value}'"  # Aspa simples para valores de string
            if column == "smape":
                where_clauses.append(f"{column} <= {value}")
                continue
            where_clauses.append(f"{column} = {value}")

        where_clause = " AND ".join(where_clauses)

        # Executar a consulta com a cláusula WHERE dinâmica
        try:
            query = f"SELECT * FROM {kwargs.get('table')} WHERE {where_clause}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao selecionar dados da tabela {kwargs.get('table')}: {e}")

    def close_connection(self):
        self.connection.close()
        print("Conexão com o banco de dados fechada com sucesso!")