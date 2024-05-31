import os
import pandas as pd
from datetime import date

class Dados_Mercado:
    def __init__(self, dataset: str, produto: int, data_inicio:date, data_fim:date):
        self.dataset = dataset
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.produto = produto

    def exibir(self):
        if not os.path.exists(self.dataset):
            print(f"Arquivo '{self.dataset}' não encontrado.")
            return None
        try:
            df_mercado = pd.read_csv(self.dataset, delimiter=',', encoding='UTF-8', low_memory=False)
            print(f"Leitura do arquivo {self.dataset} realizada com sucesso!")
            return df_mercado
        except FileNotFoundError:
            print('Arquivo não encontrado.')
        except pd.errors.EmptyDataError:
            print('O arquivo está vazio.')
        except Exception as e:
            print(f'Erro ao ler o arquivo: {e}')
        return None
    
    def analise_mercado(self):
        df_mercado = self.exibir()
        if df_mercado is None or df_mercado.empty:
            return None
        
        select_produto = self.produto
        df_mercado = df_mercado[df_mercado['item_nbr'] == select_produto]

        return df_mercado,select_produto
    
    def select_colunas(self):
        df_mercado, select_produto = self.analise_mercado()
        if df_mercado is None or df_mercado.empty:
            return None
        
        df_mercado2 = df_mercado[['date','item_nbr','unit_sales','price','day_of_week']].copy()
        df_mercado2['date'] = pd.to_datetime(df_mercado2['date'])
        return df_mercado2
    
    def remove_duplicados(self):
        df_mercado = self.select_colunas()
        if df_mercado is None or df_mercado.empty:
            return None
        
        df_mercado['unit_sales'] = df_mercado.groupby('date')['unit_sales'].transform('sum')
        df_mercado = df_mercado.drop_duplicates(keep='last')
        return df_mercado

    def selecionar_periodo(self):
        df_mercado = self.remove_duplicados()
        if df_mercado is None or df_mercado.empty:
            return None
        
        df_mercado = df_mercado[
            (df_mercado['date'] >= pd.Timestamp(self.data_inicio)) & 
            (df_mercado['date'] < pd.Timestamp(self.data_fim))
        ]
        df_exatos = self.remove_duplicados()
        df_exatos = df_exatos[df_exatos['date'] >= pd.Timestamp(self.data_fim)]
        return df_mercado,df_exatos
    
    def dados_prompt(self):
        df_mercado,df_exatos = self.selecionar_periodo()
        if df_mercado is None or df_mercado.empty:
            return None
        
        dados_prompt = df_mercado['unit_sales'].to_list()
        dados_prompt = [round(x,3) for x in dados_prompt]

        dados_exatos = df_exatos['unit_sales'].to_list()
        dados_exatos = [round(x,3) for x in dados_exatos]

        return df_mercado, dados_prompt, dados_exatos, df_exatos