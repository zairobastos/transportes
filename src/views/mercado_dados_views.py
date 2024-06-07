from typing import Optional, Tuple
from src.controllers.mercado_dados_controller import MercadoDadosController
from src.models.mercado_dados_models import DadosMercadoModels
import pandas as pd

class DadosMercadoView:

    @classmethod
    def executar(cls, dados_mercado: DadosMercadoModels) -> Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]:
        """Executa o fluxo de exibição e análise dos dados de mercado.

        Args:
            dados_mercado (DadosMercadoModels): DadosMercadoModels contendo as informações do dataset e filtros.

        Returns:
            Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]: Dataframe com os dados do prompt,
            dados do prompt, dados exatos e dataframe com os dados exatos.
        """            
        df_mercado = MercadoDadosController.exibir(dados_mercado)
        if not cls.verifica(df_mercado):
            print("Nenhum dado encontrado no dataset.")
            return None

        df_mercado = MercadoDadosController.analise_mercado(df_mercado, dados_mercado.produto)
        if not cls.verifica(df_mercado):
            print(f"Nenhum dado encontrado para o produto.")
            return None

        df_mercado = MercadoDadosController.select_colunas(df_mercado)
        if not cls.verifica(df_mercado):
            print("Nenhum dado encontrado após selecionar as colunas.")
            return None
        
        df_mercado = MercadoDadosController.remove_duplicados(df_mercado)
        if not cls.verifica(df_mercado):
            print("Nenhum dado encontrado após remover duplicados.")
            return None
        
        df_mercado, df_exatos = MercadoDadosController.selecionar_periodo(df_mercado, dados_mercado.data_inicio, dados_mercado.data_fim)
        if not cls.verifica(df_mercado) or not cls.verifica(df_exatos):
            print("Nenhum dado encontrado após selecionar o período.")
            return None
        
        dados_prompt, dados_exatos = MercadoDadosController.dados_prompt(df_mercado, df_exatos)

        return df_mercado, dados_prompt, dados_exatos, df_exatos
    
    @staticmethod
    def verifica(dataset: pd.DataFrame) -> bool:
        """Verifica se o dataset é válido e não está vazio.
        
        Args:
            dataset(pd.Dataframe): DataFrame a ser verificado.

        Returns:
            bool: Retorna True se o dataset for válido e não estiver vazio.
        """
        if dataset is None or dataset.empty:
            return False
        return True