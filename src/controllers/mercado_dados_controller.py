import os
from typing import Optional, Tuple
import pandas as pd
from datetime import date

from src.models.mercado_dados_models import DadosMercadoModels

class MercadoDadosController:
    @classmethod
    def exibir(cls, dados_mercado: DadosMercadoModels) -> pd.DataFrame:
        """Faz a leitura do arquivo de dataset enviado

        Args:
            dados_mercado (DadosMercadoModels): recebe o caminho do dataset, o produto e as datas de inicio e fim

        Returns:
            pd.DataFrame: retorna a leitura do dataset
        """
        dataset = dados_mercado.dataset      
        if not os.path.exists(dataset):
            print(f"Arquivo '{dataset}' não encontrado.")
            return None
        try:
            df_mercado = pd.read_csv(dataset, delimiter=',', encoding='UTF-8', low_memory=False)
            print(f"Leitura do arquivo {dataset} realizada com sucesso!")
            return df_mercado
        except FileNotFoundError:
            print('Arquivo não encontrado.')
        except pd.errors.EmptyDataError:
            print('O arquivo está vazio.')
        except Exception as e:
            print(f'Erro ao ler o arquivo: {e}')
        return None
    
    @classmethod
    def analise_mercado(cls, df_mercado:pd.DataFrame, select_produto:int) -> pd.DataFrame:
        """Seleciona o produto a ser analisado

        Args:
            df_mercado (pd.DataFrame): Dataset gerado pela função anterior
            select_produto (int): Número do produto selecionado pelo usuário

        Returns:
            pd.DataFrame: dataset com o produto selecionado e o produto
        """        
        if df_mercado is None or df_mercado.empty:
            return None, None
        
        df_mercado = df_mercado[df_mercado['item_nbr'] == select_produto]

        return df_mercado
    
    @classmethod
    def select_colunas(cls, df_mercado:pd.DataFrame) -> pd.DataFrame:
        """Seleciona as colunas necessárias para a análise

        Args:
            df_mercado (pd.DataFrame): Dataset gerado na função anterior

        Returns:
            pd.DataFrame: retorna o dataset com as colunas selecionadas
        """        
        if df_mercado is None or df_mercado.empty:
            return None
        
        df_mercado2 = df_mercado[['date','item_nbr','unit_sales','price','day_of_week']].copy()
        df_mercado2['date'] = pd.to_datetime(df_mercado2['date'])
        return df_mercado2
    
    @classmethod
    def remove_duplicados(cls,df_mercado:pd.DataFrame) -> pd.DataFrame:
        """Remove os duplicados do dataset

        Args:
            df_mercado (pd.DataFrame): Dataset gerado na função anterior

        Returns:
            pd.DataFrame: retorna o dataset sem duplicados
        """        
        if df_mercado is None or df_mercado.empty:
            return None
        
        df_mercado['unit_sales'] = df_mercado.groupby('date')['unit_sales'].transform('sum')
        df_mercado = df_mercado.drop_duplicates(keep='last')
        return df_mercado

    @classmethod
    def selecionar_periodo(cls,df_mercado:pd.DataFrame, data_inicio:date, data_fim:date) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Seleciona o período de análise

        Args:
            df_mercado (pd.DataFrame): Dataset gerado na função anterior
            data_inicio (date): Data de início da análise
            data_fim (date): Data de término da análise

        Returns:
            Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]: retorna o dataset com o período selecionado e o dataset com os dados exatos
        """               
        if df_mercado is None or df_mercado.empty:
            return None, None
        
        df_mercado2 = df_mercado[
            (df_mercado['date'] >= pd.Timestamp(data_inicio)) & 
            (df_mercado['date'] < pd.Timestamp(data_fim))
        ]

        df_exatos = df_mercado[df_mercado['date'] >= pd.Timestamp(data_fim)]
        return df_mercado2, df_exatos
    
    @classmethod
    def dados_prompt(cls,df_mercado:pd.DataFrame, df_exatos:pd.DataFrame) -> Tuple[Optional[list], Optional[list]]:
        """Seleciona os dados para a análise

        Args:
            df_mercado (pd.DataFrame): Dataset gerado na função anterior
            df_exatos (pd.DataFrame): Dataset gerado na função anterior

        Returns:
            Tuple[Optional[list], Optional[list]]: retorna o dataset com os dados do prompt e os dados exatos 
        """        
        if df_mercado is None or df_mercado.empty:
            return None
        
        dados_prompt = df_mercado['unit_sales'].to_list()
        dados_prompt = [round(x,3) for x in dados_prompt]

        dados_exatos = df_exatos['unit_sales'].to_list()
        dados_exatos = [round(x,3) for x in dados_exatos]

        return dados_prompt, dados_exatos