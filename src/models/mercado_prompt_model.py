import pandas as pd
from datetime import date

class PromptMercadoModels:
    def __init__(self, dataset: pd.DataFrame, exatos: list, dados_prompt: list,  df_exato: pd.DataFrame, dias:int):
        """ Inicializa uma nova instância da classe PromptMercadoModels.

        Args:
            dataset (pd.DataFrame): Dataset contendo os dados de mercado.
            exatos (list): Lista de valores exatos.
            dados_prompt (list): Dados da série temporal que vão no prompt.
            data_inicio (date): Data de início da série temporal.
            data_fim (date): Data de fim da série temporal.
            produto (int): Código do produto a ser analisado.
            df_exato (pd.DataFrame): Dataset contendo os dados exatos.
            dias (int): Quantos dias vão ser previstos.
        """        
        self.dataset = dataset
        self.exatos = exatos
        self.df_exato = df_exato
        self.dias = dias
        self.dados_prompt = dados_prompt