import streamlit as st
from datetime import date
from mercado.prompt import Prompt_Mercado
import pandas as pd
class Prompts_Mercado:
    def __init__(self, dataset: pd.DataFrame, exatos: list, dados_prompt: list, data_inicio: date, data_fim: date, produto: int, df_exato: pd.DataFrame, dias:int):
        self.dataset = dataset
        self.exatos = exatos
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.produto = produto
        self.df_exato = df_exato
        self.dias = dias
        self.dados_prompt = dados_prompt

    def prompt_view(self):
        st.write('---')
        st.write('### Prompt')
        result = Prompt_Mercado(self.dataset, self.exatos, self.dados_prompt, self.data_inicio, self.data_fim, self.produto, self.df_exato[:self.dias], self.dias).prompt()
        st.code(result, language='python',line_numbers=True)

        return result