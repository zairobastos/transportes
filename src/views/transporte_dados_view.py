from typing import Optional, Tuple
from src.controllers.transporte_dados_controller import DadosTransporteController
from src.models.transporte_dados_models import DadosTransporteModels
import pandas as pd

class DadosTransporteView:
    @classmethod
    def executar(cls, dados_transporte: DadosTransporteModels) -> Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]:
        """Executa o fluxo de exibição e análise dos dados de transporte.

        Args:
            dados_transporte (DadosTransporteModels): DadosTransporteModels contendo as informações do dataset e filtros.

        Returns:
            Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]: dataframe contendo o intervalo de 
            datas selecionados, uma lista com os passageiros desse dataframe,uma lista contendo os próximos 168 valores 
            e o datframe com esses valores.
        """               
        # Exibir dados de transporte
        df_transport = DadosTransporteController.exibir(dados_transporte)
        if not cls.verifica(df_transport):
            print("Nenhum dado encontrado no dataset.")
            return None, [], [], None

        # Analisar linhas de ônibus
        df_linha = DadosTransporteController.analise_linhas(df_transport, dados_transporte.linhas_onibus)
        if not cls.verifica(df_linha):
            print(f"Nenhum dado encontrado para a linha de ônibus.")
            return None, [], [], None

        # Selecionar dados por data
        df_linha_filtrada = DadosTransporteController.select_data(df_linha)
        if not cls.verifica(df_linha_filtrada):
            print("Nenhum dado encontrado após aplicar os filtros de data.")
            return None, [], [], None

        # Remover duplicados
        df_linha_sem_duplicados = DadosTransporteController.remove_duplicados(df_linha_filtrada)
        if not cls.verifica(df_linha_sem_duplicados):
            print("Nenhum dado encontrado após remover duplicados.")
            return None, [], [], None

        # Adicionar valores faltantes
        dataset_semifinal = DadosTransporteController.add_valores_faltantes(df_linha_sem_duplicados)
        if not cls.verifica(dataset_semifinal):
            print("Nenhum dado encontrado após adicionar valores faltantes.")
            return None, [], [], None

        # Selecionar dados finais
        dataset_final, passageiros, exato, df_exato = DadosTransporteController.selecionar_dados_prompt(dataset_semifinal, dados_transporte.data_inicio, dados_transporte.data_fim)
        print(dataset_final)
        return dataset_final, passageiros, exato, df_exato

    @staticmethod
    def verifica(dataset: pd.DataFrame) -> bool:
        """Verifica se o dataset é válido e não está vazio.
        
        Args:
            dataset(pd.Dataframe): DataFrame a ser verificado.

        Returns:
            bool: True se o DataFrame não está vazio e não é None, caso contrário False
        """        
        return dataset is not None and not dataset.empty
