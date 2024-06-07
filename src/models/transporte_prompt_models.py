import pandas as pd
from datetime import date
class PromptTransporteModels:
    def __init__(self, dataset:pd.DataFrame, dados_prompt:list, dados_exato:list, data_inicio:date, data_fim:date,linha_onibus:int,df_exato:pd.DataFrame, horas:int=24):
        """ Inicializa uma nova instância da classe Prompt.

        Args:
            dataset (pd.DataFrame): Recebe o dataset contendo os dados de transporte.
            dados_prompt (list): Dados da serie temporal que vão no prompt
            dados_exato (list): Dados da serie temporal que vai ser comparada com o que foi previsto
            data_inicio (date): data de inicio da serie temporal
            data_fim (date): data de fim da serie temporal
            linha_onibus (int): linha de onibus que vai ser analisada
            df_exato (pd.DataFrame): dataset contendo os dados exatos
            horas (int, optional): Quantas horas vão ser previstas. Defaults to 24.
        """        
        self.dataset = dataset
        self.dados_prompt = dados_prompt
        self.dados_exato = dados_exato
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.linha_onibus = linha_onibus
        self.df_exato = df_exato
        self.horas = horas