import pandas as pd
from datetime import date

class DadosMercadoModels:
    def __init__(self, dataset: str, produto: int, data_inicio:date, data_fim:date):
        """Inicializa uma nova instância da classe DadosMercadoModels.

        Args:
            dataset (str): Dataset contendo os dados de mercado.
            produto (int): Número do produto a ser analisado.
            data_inicio (date): Data de início do período de análise.
            data_fim (date): Data de término do período de análise.
        """        
        self.dataset = dataset
        self.data_inicio = pd.to_datetime(data_inicio)
        self.data_fim = pd.to_datetime(data_fim)
        self.produto = produto