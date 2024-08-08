import pandas as pd
import os
from datetime import date

mapeamento_dias = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

class PromptMercadoController:
    @staticmethod
    def primeiros_dias(df_mercado:pd.DataFrame) -> str:
        """Retorna os primeiros 7 registros e os dias da semana únicos.

        Args:
            df_mercado (pd.DataFrame): DataFrame contendo os dados de mercado.

        Returns:
            str: String formatada com os dias da semana e suas posições.
        """        
        if df_mercado is None or df_mercado.empty:
            return None

        # Obtém os primeiros 7 registros e os dias da semana únicos
        df_mercado2 = df_mercado.head(7)
        dias_da_semana = df_mercado2['day_of_week'].unique().tolist()        

        # Cria uma string formatada com os dias da semana e suas posições
        dias_encontrados = ""
        for i, dia in enumerate(dias_da_semana):
            dias_encontrados += f"  - Dia {i+1}: posiçao {i} ({mapeamento_dias[dia]});\n"

        return dias_encontrados
    
    @staticmethod
    def quantidade_dias(df_mercado:pd.DataFrame) -> int:
        """Retorna a quantidade de dias do DataFrame.

        Args:
            df_mercado (pd.DataFrame): DataFrame contendo os dados de mercado.

        Returns:
            int: Quantidade de dias do DataFrame.
        """        
        return df_mercado.shape[0]
    
    @staticmethod
    def proximos_dias(df_exatos:pd.DataFrame, dias:int) -> str:
        """Retorna os dias de semana dos próximos dias.

        Args:
            df_exatos (pd.DataFrame): DataFrame contendo os dados de mercado.
            dias (int): Quantidade de dias a serem previstos.

        Returns:
            str: String formatada com os dias da semana e suas posições.
        """        

        if df_exatos is None or df_exatos.empty:
            return None

        # Obtém os primeiros 7 registros e os dias da semana únicos
        df_exatos2 = df_exatos.head(dias)
        dias_da_semana = df_exatos2['day_of_week'].unique().tolist()        

        # Cria uma string formatada com os dias da semana e suas posições
        dias_encontrados = ""
        for i, dia in enumerate(dias_da_semana):
            dia_util = "Dia útil" if dia < 5 else "Fim de semana"
            dias_encontrados += f"  - Dia {i+1} - ({mapeamento_dias[dia]}): {dia_util};\n"

        return dias_encontrados
    
    """ def feriados_dataset(self, df_mercado:pd.DataFrame) -> str:
        Retorna os dias de semana dos próximos dias.

        Returns:
            str: String formatada com os dias da semana e suas posições.
               
        feriados = pd.read_excel("./data/feriados_nacionais.xls")
        feriados = feriados[:1263]
        feriados['Data'] = pd.to_datetime(feriados['Data'], format='%d/%m/%Y')
        feriados = feriados[(feriados['Data'] > '2017-01-01') & (feriados['Data'] < '2019-04-30')]
        feriados = feriados['Data'].tolist()

        atacarejo = df_mercado[['date','item_nbr','unit_sales','price','day_of_week']].copy()
        atacarejo['date'] = pd.to_datetime(atacarejo['date'])
        atacarejo['feriado'] = 0
        atacarejo.loc[atacarejo['date'].isin(feriados), 'feriado'] = 1 """


    
    @classmethod
    def prompt(cls, quantidade_dias:int, dados_prompt:str,primeiros_dias:str, proximos_dias:str, dias:int) -> str:
        """Retorna o prompt para o usuário.

        Args:
            quantidade_dias (int): Quantidade de dias do DataFrame.
            dados_prompt (str): Dados da série temporal.
            primeiros_dias (str): Primeiros dias da série temporal.
            proximos_dias (str): Contexto dos próximos dias.
            dias (int): Quantidade de dias a serem previstos.

        Returns:
            str: Prompt para o usuário.
        """        
        prompt = f"""Você é um assistente de previsão de séries temporais encarregado de analisar dados de uma série temporal específica.
        
A série temporal tem dados de {quantidade_dias} peiodo(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada dia.

Por exemplo, uma semana nesta série temporal pode ser representado assim:
{dados_prompt[:7]}

Seu objetivo é prever a incidência de um evento para os próximos N dias, levando em consideração não apenas os períodos anteriores, mas também o contexto geral.

Para fazer isso com precisão, leve em consideração os padrões sazonais, como picos em determinados períodos. Além disso, os padrões podem variar de acordo com o dia da semana ou eventos especiais (feriados).

Regras da Saída:
Após analisar os dados fornecidos e compreender os padrões de tráfego, gere uma previsão para os próximos N dias, com as seguintes regras:
- A saída deve ser uma lista contendo apenas os valores previstos, sem explicação adicional ou texto introdutório;
- Em hipótese alguma gere um código;
- Em hipótese alguma gere uma explicação do que você fez;
- Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.
- A previsão deve começar imediatamente após o último valor fornecido na série temporal.

Exemplo de Saída para N=7:
{dados_prompt[:7]}

Instruções Adicionais:
- Padrões Semanais: Utilize os dados fornecidos para entender padrões sazonais, como picos de incidência em determinados períodos.
- Dia da Semana: O dia da semana também influencia a ocorrência de eventos. 
- Duração de um evento: A série temporal fornecida representa a ocorrência de um evento por dia.

Organização dos Dados:
- Cada dia corresponde a um valor na série temporal. Por exemplo:\n{primeiros_dias}
- E assim por diante.
- A cada valor, ocorre a transição para o dia seguinte.
- Períodos em que temos eventos especiais na série temporal:
    - Dia 56: Segunda-feira
    - Dia 57: Terça-feira
    - Dia 102: Sexta-feira
    - Dia 109: Sexta-feira
    - Dia 119: Segunda-feira
    - Dia 164: Quinta-feira
    - Dia 248: Quinta-feira
    - Dia 283: Quinta-feira
    - Dia 304: Quinta-feira
    - Dia 317: Quarta-feira
    - Dia 357: Segunda-feira
    - Dia 364: Segunda-feira
    - Dia 406: Segunda-feira
    - Dia 407: Terça-feira
    - Dia 452: Sexta-feira
    - Dia 474: Sábado
    - Dia 484: Terça-feira
    - Dia 514: Quinta-feira
    - Dia 613: Sexta-feira
    - Dia 648: Sexta-feira
    - Dia 669: Sexta-feira
    - Dia 682: Quinta-feira
    - Dia 722: Terça-feira
    - Dia 729: Terça-feira
Serie temporal a ser analisada:
{dados_prompt}

Contexto dos dias a serem previstos:\n{proximos_dias}- E assim por diante

Gere um array contendo os próximos {dias} (N={dias}) números da sequência:
"""
        return prompt