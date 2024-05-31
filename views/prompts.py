import streamlit as st
from datetime import date
from transporte.prompt import Prompt
import pandas as pd
class Prompts:
    def __init__(self, dataset: pd.DataFrame, passageiros: list[int], exatos: list[int], data_inicio: date, data_fim: date, linhas_onibus: int, df_exato: pd.DataFrame, horas:int):
        self.dataset = dataset
        self.passageiros = passageiros
        self.exatos = exatos
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.linhas_onibus = linhas_onibus
        self.df_exato = df_exato
        self.horas = horas

    def prompt_view(self):
        st.write('---')
        st.write('### Prompt')
        result = Prompt(self.dataset, self.passageiros, self.exatos, self.data_inicio, self.data_fim, self.linhas_onibus, self.df_exato[:self.horas], self.horas)
        st.code(result.arquivos_prompt(), language='python',line_numbers=True)

        return result.arquivos_prompt()