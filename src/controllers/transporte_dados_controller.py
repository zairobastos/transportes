# src/controllers/transporte_dados_controller.py
import os
import pandas as pd
from datetime import date
from src.models.transporte_dados_models import DadosTransporteModels

class DadosTransporteController:
    @classmethod
    def exibir(cls, dados_transporte: DadosTransporteModels) -> pd.DataFrame:
        """Faz a leitura do arquivo de dataset enviado

        Args:
            dados_transporte (DadosTransporteModels): recebe o caminho do dataset, a linha de ônibus e as datas de inicio e fim

        Returns:
            pd.Dataframe: retorna a leitura do dataset
        """
        dataset = dados_transporte.dataset
        if not os.path.exists(dataset):
            print(f"Arquivo '{dataset}' não encontrado.")
            return None
        try:
            df_transport = pd.read_csv(dataset, delimiter=',', encoding='UTF-8', low_memory=False)
            print(f"Leitura do arquivo {dataset} realizada com sucesso!")
            return df_transport
        except FileNotFoundError:
            print('Arquivo não encontrado.')
        except pd.errors.EmptyDataError:
            print('O arquivo está vazio.')
        except Exception as e:
            print(f'Erro ao ler o arquivo: {e}')
        return None

    @classmethod
    def analise_linhas(cls, df_transport:pd.DataFrame, linhas_onibus:int) -> tuple:
        """Função responsável por selecionar a linha de ônibus

        Args:
            df_transport (pd.DataFrame): Dataset gerado pela função anterior
            linhas_onibus (int): Número da linha de ônibus selecionada pelo usuário

        Returns:
            tuple: dataset com a linha selecionada e a linha de ônibus
        """        
        if df_transport is None or df_transport.empty:
            return None, None
        
        top_linhas = df_transport.groupby('linha')['validations_per_hour'].sum().sort_values(ascending=False).head(10)
        df_linha = df_transport[df_transport['linha'] == linhas_onibus]

        return df_linha, linhas_onibus
    
    @classmethod
    def select_data(cls, df_linha:pd.DataFrame) -> pd.DataFrame:
        """Simplifica o dataset anterior colocando apenas as colunas úteis

        Args:
            df_linha (pd.DataFrame): Dataset gerado na função anterior

        Returns:
            pd.Dataframe: retorna um dataset com a linha selecionada pelo usuário e as colunas mais importantes
        """        
        if df_linha is None or df_linha.empty:
            return None

        df_linha2 = df_linha[['data_hora','d_semana','validations_per_hour', 'feriado','vespera_feriado']].copy()
        df_linha2['data_hora'] = pd.to_datetime(df_linha2['data_hora'])

        return df_linha2
    
    @classmethod
    def remove_duplicados(cls,df_linha2:pd.DataFrame) -> pd.DataFrame:
        """Responsável por somar os valores dúplicados e remover a maioria deixando apenas um valor único

        Args:
            df_linha2 (pd.DataFrame): Dataset simplificado da função anterior

        Returns:
            pd.DataFrame: Um novo dataset sem a repetição de valores
        """        
        if df_linha2 is None or df_linha2.empty:
            return None
        
        df_linha2['validations_per_hour'] = df_linha2.groupby('data_hora')['validations_per_hour'].transform('sum')
        df_linha2 = df_linha2.drop_duplicates(keep='last')

        return df_linha2
    
    @staticmethod
    def create_dataset(ano:int=2018, meses:list[int]=range(1, 8)) -> pd.DataFrame:
        """Cria um dataset com anos, meses, dias e horas, afim de que todas as linhas siga o padrão de ter todas as horas

        Args:
            ano (int, optional): _description_. Defaults to 2018.
            meses (list[int], optional): _description_. Defaults to range(1, 8).

        Returns:
            pd.DataFrame: retorna um dataframe novo
        """        
        datas = []
        for mes in meses:
            for dia in range(1, 29 if mes == 2 else 31 if mes in [4, 6] else 32):
                for hora in range(24):
                    datas.append(pd.Timestamp(ano, mes, dia, hora))

        df = pd.DataFrame({'data_hora': datas})
        return df
    
    @staticmethod
    def feriados(dataset:pd.DataFrame) -> list:
        """Gera uma lista com todos os feriados do dataset selecionado

        Args:
            dataset (pd.DataFrame): dataset que é passado quando a função for chamada

        Returns:
            list: lista contendo todas as datas em que se é feriado
        """        
        df_transport = dataset
        if df_transport is None or df_transport.empty:
            return None

        feriados = df_transport[df_transport['feriado'] == 1]
        if feriados.empty:
            print("Nenhum feriado encontrado no DataFrame.")
            return [] 

        datas_feriados = feriados['data_hora'].dt.date.unique().tolist()
        
        return datas_feriados
    
    @staticmethod
    def vespera_feriado(dataset:pd.DataFrame) -> list:
        """Gera uma lista com todas as vésperas de feriados do dataset selecionado

        Args:
            dataset (pd.DataFrame): dataset que é passado quando a função for chamada

        Returns:
            list: lista contendo todas as datas em que se é véspera de feriado
        """        
        df_transport = dataset
        if df_transport is None or df_transport.empty:
            return None
        vespera_feriado = df_transport[df_transport['vespera_feriado'] == 1]
        if vespera_feriado.empty:
            print("Nenhuma véspera de feriado encontrada no DataFrame.")
            return []
        
        datas = vespera_feriado['data_hora'].dt.date.unique().tolist()
        return datas
    
    @classmethod
    def add_valores_faltantes(cls,df_linha2:pd.DataFrame) -> pd.DataFrame:        
        """Adiona valores que estão faltando ao dataset

        Args:
            df_linha2 (pd.DataFrame): Trata-se do Dataset em que foram excluido os valores duplicados

        Returns:
            pd.DataFrame: Retorna um novo dataset contendo 
        """        
        df_completo = cls.create_dataset()
        if df_completo is None or df_completo.empty:
            return None
        
        df_transport2 = pd.merge(df_completo, df_linha2, on='data_hora', how='left').fillna(0)
        df_transport2['d_semana'] = df_transport2['data_hora'].dt.dayofweek
        df_transport2['feriado'] = df_transport2['data_hora'].dt.date.isin(cls.feriados(df_transport2)).astype(int)
        df_transport2['vespera_feriado'] = df_transport2['data_hora'].dt.date.isin(cls.vespera_feriado(df_transport2)).astype(int)

        df_transport2['validations_per_hour'] = df_transport2['validations_per_hour'].astype(int)
        df_transport2.reset_index(drop=True, inplace=True) 
        return df_transport2
    
    @classmethod
    def selecionar_dados_prompt(cls,df_transport:pd.DataFrame, data_inicio:date, data_fim:date)-> tuple:
        """Gera o dataset final

        Args:
            df_transport (pd.DataFrame): Dataset com tudo ajustado
            data_inicio (date): data de inicio
            data_fim (date): data de fim
        
        Returns:
            tuple: dataframe contendo o intervalo de datas selecionados, uma lista com os passageiros desse dataframe,
            uma lista contendo os próximos 168 valores e o datframe com esses valores.
        """        
        if df_transport is None or df_transport.empty:
            return None, [], [], None
        
        
        data_inicio = str(data_inicio)
        data_fim = str(data_fim)
        
        df_selecionado = df_transport[(df_transport['data_hora'] >= data_inicio) & (df_transport['data_hora'] < data_fim)]
        passageiros = df_selecionado['validations_per_hour'].values.tolist()

        df_exato = df_transport[df_transport['data_hora'] >= data_fim].head(168)
        exato = df_exato['validations_per_hour'].values.tolist()

        return df_selecionado, passageiros, exato, df_exato
    
