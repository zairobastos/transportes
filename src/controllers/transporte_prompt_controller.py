import pandas as pd
import os
from src.models.transporte_prompt_models import PromptTransporteModels

mapeamento_dias = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

class PromptTransporteController:

    @staticmethod
    def primeiros_dias(df_transport:pd.DataFrame) -> str:
        """Retorna os primeiros 168 registros e os dias da semana únicos.

        Args:
            df_transport (pd.DataFrame): DataFrame contendo os dados de transporte.

        Returns:
            str: String formatada com os dias da semana e suas posições.
        """        
        if df_transport is None or df_transport.empty:
            return None

        # Obtém os primeiros 168 registros e os dias da semana únicos
        df_transport2 = df_transport.head(168)
        dias_da_semana = df_transport2['d_semana'].unique().tolist()        

        # Cria uma string formatada com os dias da semana e suas posições
        dias_encontrados = ""
        for i, dia in enumerate(dias_da_semana):
            pos_inicio = i * 24
            pos_fim = pos_inicio + 23
            dias_encontrados += f"  - Dia {i+1}: posições {pos_inicio} a {pos_fim} ({mapeamento_dias[dia]});\n"

        return dias_encontrados
    
    @staticmethod
    def feriados(df_transport:pd.DataFrame) -> str:
        """Retorna os dias de feriados encontrados no DataFrame.

        Args:
            df_transport (pd.DataFrame): DataFrame contendo os dados de transporte.

        Returns:
            str: String formatada com os dias de feriados e suas posições.
        """        
        if df_transport is None or df_transport.empty:
            return None
        df_transport = df_transport.reset_index(drop=True)
        dataset_feriados = df_transport[df_transport['feriado'] == 1]
        if dataset_feriados.empty:
            print("Nenhum feriado encontrado no DataFrame.")
            return []
        
        list_datas_feriados = dataset_feriados['data_hora'].dt.date.unique().tolist()
        dias_feriados = ""
        for data in list_datas_feriados:
            indices_dia = dataset_feriados[dataset_feriados['data_hora'].dt.date == data].index.tolist()
            dia = indices_dia[0] // 24 + 1  # Calcula o número do dia
            dias_feriados += f"  - Dia {dia}: posições {indices_dia[0]} a {indices_dia[-1]} ({mapeamento_dias[data.weekday()]});\n"

        return dias_feriados
    
    def proximos_dias(df_exato:pd.DataFrame) -> str:
        """Retorna o contexto dos dias a serem previstos.

        Args:
            df_exato (pd.DataFrame): DataFrame contendo os dados de transporte.

        Returns:
            str: Contexto dos dias a serem previstos.
        """        
        if df_exato is None or df_exato.empty:
            return None
            
        list_datas_proximos_dias = df_exato['data_hora'].dt.date.unique().tolist()
        dias_proximos = ""
        for i, data in enumerate(list_datas_proximos_dias):
            pos_inicio = i * 24
            pos_fim = pos_inicio + 23
            dia_util = "Dia útil" if data.weekday() < 5 else "Final de semana"
            if df_exato[df_exato['data_hora'].dt.date == data]['feriado'].values[0] == 1:
                dia_util = "Feriado"
            dias_proximos += f"Dia {i+1} - {mapeamento_dias[data.weekday()]} (posições {pos_inicio}-{pos_fim} da sua previsão): {dia_util};\n"
        return dias_proximos
    
    @staticmethod
    def ultimo_dia(df_transport:pd.DataFrame) -> str:
        """Retorna o dia da semana do último dia do DataFrame.

        Args:
            df_transport (pd.DataFrame): DataFrame contendo os dados de transporte.

        Returns:
            str: Dia da semana do último dia do DataFrame.
        """        
        if df_transport is None or df_transport.empty:
            return None
        return mapeamento_dias[df_transport['d_semana'].iloc[-1]]
    
    @staticmethod
    def quantidade_dias(df_transport:pd.DataFrame) -> int:
        """Retorna a quantidade de dias do DataFrame.

        Args:
            df_transport (pd.DataFrame): DataFrame contendo os dados de transporte.

        Returns:
            int: Quantidade de dias do DataFrame.
        """        
        if df_transport is None or df_transport.empty:
            return None
        
        shape = df_transport.shape[0]
        dias = shape // 24
        return dias
    
    @classmethod
    def prompt(cls, quantidade_dias:int, feriados:str, proximos_dias:str, dados_prompt: list, primeiros_dias:str,  horas:int) -> str:
        """Retorna o prompt para o desafio.

        Args:
            quantidade_dias (int): Quandidade de dias que estão na serie temporal
            feriados (str): Descrição dos dias que são feriados
            proximos_dias (str): Descrição dos dias a serem previstos
            dados_prompt (list): Dados da serie temporal
            horas (int): Quantidade de horas a serem previstas
            primeiros_dias (str): Descrição dos primeiros dias da serie temporal

        Returns:
            str: Prompt para a LLM.
        """              
        controller_prompt = PromptTransporteController()
        prompt = f"""Você é um assistente de previsão de séries temporais encarregado de analisar dados de uma série temporal específica.
        
A série temporal tem dados de {quantidade_dias} dia(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada hora de um dia.

Por exemplo, um dia nesta série temporal pode ser representado assim:
{dados_prompt[:24]}

Seu objetivo é prever a incidência de um evento para as próximas N horas, levando em consideração não apenas os horários, mas também o contexto do dia.

Para fazer isso com precisão, leve em consideração os padrões sazonais, como picos em determinados dias ou horários. Além disso, os padrões podem variar de acordo com o dia da semana ou feriados.

Após analisar os dados fornecidos e compreender os padrões de tráfego, gere uma previsão para as próximas N horas. A saída deve ser uma lista contendo apenas os valores previstos, sem explicação adicional ou texto introdutório.

Regras da Saída:
- Em hipótese alguma gere um código;
- Em hipótese alguma gere uma explicação do que você fez;
- Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.

Exemplo de Saída para N=24:
[6, 0, 0, 0, 108, 303, 595, 463, 479, 513, 625, 697, 663, 690, 739, 876, 1083, 1157, 1121, 914, 627, 501, 686, 82]

Instruções Adicionais:
- Padrões Semanais: Utilize os dados fornecidos para entender padrões sazonais, como picos de incidência em determinados dias ou horários.
- Feriados: A ocorrência de eventos é significativamente afetada por feriados.
- Dia da Semana: O dia da semana também influencia a ocorrência de eventos. Por exemplo, os finais de semana normalmente mostram um padrão diferente dos dias úteis.
- Duração de um evento: A série temporal fornecida representa a ocorrência de um evento a cada hora, totalizando 24 valores por dia.

Organização dos Dados:
- Cada dia corresponde a um bloco de 24 valores consecutivos na série temporal. Por exemplo:\n{primeiros_dias}
- E assim por diante.
- A cada 24 valores, ocorre a transição para o dia seguinte.
- Dias em que temos feriado na série temporal:\n{feriados}

Serie temporal a ser analisada:
{dados_prompt}

Contexto dos dias a serem previstos:\n{proximos_dias}

Gere um array contendo os próximos {horas} (N={horas}) números da sequência:
"""
        return prompt