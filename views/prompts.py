import streamlit as st
from datetime import date
from src.models.transporte_prompt_models import PromptTransporteModels
import pandas as pd

from src.views.transporte_prompt_view import PromptTransporteView
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
        dados_model_prompt = PromptTransporteModels(
            dataset=self.dataset, 
            dados_prompt=self.passageiros, 
            dados_exato=self.exatos, 
            data_inicio=self.data_inicio, 
            data_fim=self.data_fim, 
            linha_onibus=self.linhas_onibus, 
            df_exato=self.df_exato, 
            horas=self.horas
        )
        result = PromptTransporteView().exibirPrompt(dados_model_prompt)
        st.code(result, language='python',line_numbers=True)

        return result