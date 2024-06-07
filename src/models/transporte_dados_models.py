import pandas as pd
from datetime import date

class DadosTransporteModels:
    def __init__(self, dataset: pd.DataFrame, linhas_onibus: int, data_inicio: date, data_fim: date):
        """
        Inicializa uma nova instância da classe DadosTransporteModels.

        Args:
            dataset (pd.DataFrame): O dataset contendo os dados de transporte.
            linhas_onibus (int): O número da linha de ônibus a ser analisada.
            data_inicio (date): A data de início do período de análise.
            data_fim (date): A data de término do período de análise.
        """
        self.dataset = dataset
        self.linhas_onibus = int(linhas_onibus)
        self.data_inicio = pd.to_datetime(data_inicio)
        self.data_fim = pd.to_datetime(data_fim)
