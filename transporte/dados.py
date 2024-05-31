# Bibliotecas utilizadas para manipulação de dados
import os
import pandas as pd

class Dados:
    def __init__(self, dataset,linhas,data_inicio,data_fim):
        self.dataset = dataset
        self.linhas_onibus = linhas
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def exibir(self):
        if not os.path.exists(self.dataset):
            print(f"Arquivo '{self.dataset}' não encontrado.")
            return None
        try:
            df_transport = pd.read_csv(self.dataset, delimiter=',', encoding='UTF-8',low_memory=False)
            print(f"Leitura do arquivo {self.dataset} realizada com sucesso!")
            return df_transport
        except FileNotFoundError:
            print('Arquivo não encontrado.')
        except pd.errors.EmptyDataError:
            print('O arquivo está vazio.')
        except Exception as e:
            print(f'Erro ao ler o arquivo: {e}')
        return None
    
    def analise_linhas(self):
        df_transport = self.exibir()
        if df_transport is None or df_transport.empty:
            return None
        
        top_linhas = df_transport.groupby('linha')['validations_per_hour'].sum().sort_values(ascending=False).head(10)
        """ print(f'Linhas com mais passageiros: {top_linhas.index.tolist()}')
        print(f'Quantidade de passageiros: {top_linhas.values.tolist()}') """

        select_linha = self.linhas_onibus
        
        df_linha = df_transport[df_transport['linha'] == select_linha]

        return df_linha, select_linha
    
    def select_data(self):
        df_transport, linha = self.analise_linhas()
        if df_transport is None or df_transport.empty:
            return None

        df_transport2 = df_transport[['data_hora','d_semana','validations_per_hour', 'feriado','vespera_feriado']].copy()
        df_transport2['data_hora'] = pd.to_datetime(df_transport2['data_hora'])

        return df_transport2
    
    def remove_duplicados(self):
        df_transport = self.select_data()
        if df_transport is None or df_transport.empty:
            return None
        df_transport['validations_per_hour'] = df_transport.groupby('data_hora')['validations_per_hour'].transform('sum')
        df_transport = df_transport.drop_duplicates(keep='last')
        return df_transport
    
    def create_dataset(self, ano=2018, meses=range(1, 8)):
        datas = []
        for mes in meses:
            for dia in range(1, 29 if mes == 2 else 31 if mes in [4, 6] else 32):
                for hora in range(24):
                    datas.append(pd.Timestamp(ano, mes, dia, hora))

        df = pd.DataFrame({'data_hora': datas})
        return df
    
    def feriados(self,dataset):
        df_transport = dataset
        if df_transport is None or df_transport.empty:
            return None

        feriados = df_transport[df_transport['feriado'] == 1]
        if feriados.empty:
            print("Nenhum feriado encontrado no DataFrame.")
            return [] 

        datas_feriados = feriados['data_hora'].dt.date.unique().tolist()
        
        """ print("Feriados encontrados:")
        for data in datas_feriados:
            print(f"- {data.strftime('%d/%m/%Y')}")
            print(f"Índices: {feriados[feriados['data_hora'].dt.date == data].index.tolist()}")  
            print("-" * 30) """

        return datas_feriados
    
    def vespera_feriado(self,dataset):
        df_transport = dataset
        if df_transport is None or df_transport.empty:
            return None
        vespera_feriado = df_transport[df_transport['vespera_feriado'] == 1]
        if vespera_feriado.empty:
            print("Nenhuma véspera de feriado encontrada no DataFrame.")
            return []
        
        datas = vespera_feriado['data_hora'].dt.date.unique().tolist()
        """ print("Vésperas de feriado encontradas:")
        for data in datas:
            print(f"- {data.strftime('%d/%m/%Y')}")
            print(f"Índices: {vespera_feriado[vespera_feriado['data_hora'].dt.date == data].index.tolist()}")
            print("-" * 30) """
        return datas
    
    def add_valores_faltantes(self):        
        df_transport = self.remove_duplicados()
        if df_transport is None or df_transport.empty:
            return None

        df_completo = self.create_dataset()
        if df_completo is None or df_completo.empty:
            return None
        
        df_transport2 = pd.merge(df_completo, df_transport, on='data_hora', how='left').fillna(0)
        df_transport2['d_semana'] = df_transport2['data_hora'].dt.dayofweek
        df_transport2['feriado'] = df_transport2['data_hora'].dt.date.isin(self.feriados(df_transport2)).astype(int)
        df_transport2['vespera_feriado'] = df_transport2['data_hora'].dt.date.isin(self.vespera_feriado(df_transport2)).astype(int)

        df_transport2['validations_per_hour'] = df_transport2['validations_per_hour'].astype(int)
        df_transport2.reset_index(drop=True, inplace=True) 
        return df_transport2
    
    def selecionar_dados_prompt(self):
        df_transport = self.add_valores_faltantes()
        if df_transport is None or df_transport.empty:
            return None
        
        data_inicio = str(self.data_inicio)
        data_fim = str(self.data_fim)
        
        df_selecionado = df_transport[(df_transport['data_hora'] >= data_inicio) & (df_transport['data_hora'] < data_fim)]
        passageiros = df_selecionado['validations_per_hour'].values.tolist()

        df_exato = df_transport[df_transport['data_hora'] >= data_fim].head(168)
        exato = df_exato['validations_per_hour'].values.tolist()

        feriados_selecionados = self.feriados(df_selecionado.reset_index(drop=True))
        print("Dados finalizado!")

        return df_selecionado, passageiros, exato, df_exato

"""[datetime.date(2018, 1, 1), datetime.date(2018, 2, 12), datetime.date(2018, 2, 13)] 
Dia 1: posições 0 a 23 (Segunda-feira);
Dia 42: posições 1008 a 1031 (Segunda-feira);
Dia 43: posições 1032 a 1055 (Terça-feira);

2018/03/01
2018/06/04
"""