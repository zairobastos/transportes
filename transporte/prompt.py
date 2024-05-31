import pandas as pd
import os

mapeamento_dias = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

class Prompt:
    def __init__(self, dataset, dados_prompt, dados_exato, data_inicio, data_fim,linha_onibus,df_exato, horas=24):
        self.dataset = dataset
        self.dados_prompt = dados_prompt
        self.dados_exato = dados_exato
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.linha_onibus = linha_onibus
        self.df_exato = df_exato
        self.horas = horas

    def primeiros_dias(self):
        df_transport = self.dataset
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
    
    def feriados(self):
        df_transport = self.dataset
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
    
    def proximos_dias(self):
        df_transport = self.df_exato
        if df_transport is None or df_transport.empty:
            return None
            
        list_datas_proximos_dias = df_transport['data_hora'].dt.date.unique().tolist()
        dias_proximos = ""
        for i, data in enumerate(list_datas_proximos_dias):
            pos_inicio = i * 24
            pos_fim = pos_inicio + 23
            dia_util = "Dia útil" if data.weekday() < 5 else "Final de semana"
            if df_transport[df_transport['data_hora'].dt.date == data]['feriado'].values[0] == 1:
                dia_util = "Feriado"
            dias_proximos += f"Dia {i+1} - {mapeamento_dias[data.weekday()]} (posições {pos_inicio}-{pos_fim} da sua previsão): {dia_util};\n"
        return dias_proximos
    
    def ultimo_dia(self):
        df_transport = self.dataset
        if df_transport is None or df_transport.empty:
            return None
        ultimo_dia = df_transport.tail(24)
        dia = ultimo_dia['d_semana'].values[0]
        return mapeamento_dias[dia]
    
    def quantidade_dias(self):
        df_transport = self.dataset
        if df_transport is None or df_transport.empty:
            return None
        
        shape = df_transport.shape[0]
        dias = shape // 24
        return dias
    
    def prompt(self):
        prompt = f"""Você é um assistente de previsão de séries temporais encarregado de analisar dados de uma série temporal específica.
        
A série temporal tem dados de {self.quantidade_dias()} dia(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada hora de um dia.

Por exemplo, um dia nesta série temporal pode ser representado assim:
{self.dados_prompt[:24]}

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
- Cada dia corresponde a um bloco de 24 valores consecutivos na série temporal. Por exemplo:\n{self.primeiros_dias()}
- E assim por diante.
- A cada 24 valores, ocorre a transição para o dia seguinte.
- Dias em que temos feriado na série temporal:\n{self.feriados()}

Serie temporal a ser analisada:
{self.dados_prompt}

Contexto dos dias a serem previstos:\n{self.proximos_dias()}

Gere um array contendo os próximos {self.horas} (N={self.horas}) números da sequência:
"""
        return prompt
    
    def arquivos_prompt(self):
        prompt = self.prompt()
        linha = self.linha_onibus
        data_inicio = self.data_inicio
        data_fim = self.data_fim

        if not os.path.exists(f'prompts/{linha}'):
            os.mkdir(f'prompts/{linha}')
        
        arquivo = open(f'prompts/{linha}/prompt_{data_inicio}_{data_fim}.md', 'w')
        arquivo.write(prompt)
        arquivo.close()

        if os.path.exists(f'prompts/{linha}/prompt_{data_inicio}_{data_fim}.md'):
            print(f"Arquivo 'prompt_{data_inicio}_{data_fim}.md' criado com sucesso.")
        else:
            print(f"Erro ao criar o arquivo 'prompt_{data_inicio}_{data_fim}.md'.")
            return None
        
        if not os.path.exists(f'prompts/{linha}'):
            os.mkdir(f'prompts/{linha}')
        
        arquivo_exato = open(f'prompts/{linha}/exato_{data_inicio}_{data_fim}.txt', 'w')
        arquivo_exato.write(str(self.dados_exato))
        arquivo_exato.close()

        if os.path.exists(f'prompts/{linha}/exato_{data_inicio}_{data_fim}.txt'):
            print(f"Arquivo 'exato_{data_inicio}_{data_fim}.txt' criado com sucesso.")
        else:
            print(f"Erro ao criar o arquivo 'exato_{data_inicio}_{data_fim}.txt'.")
            return None

        return prompt

