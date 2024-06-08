import streamlit as st
from datetime import date
import pandas as pd

from src.models.mercado_prompt_model import PromptMercadoModels
from src.views.mercado.mercado_prompt_view import PromptMercadoView

class PromptsMercado:
    def __init__(self, dataset: pd.DataFrame, exatos: list, dados_prompt: list, produto: int, df_exato: pd.DataFrame, dias:int):
        """ Inicializa uma nova instância da classe Prompts_Mercado.

        Args:
            dataset (pd.DataFrame): Dataset contendo os dados de mercado.
            exatos (list): Lista de exatos.
            dados_prompt (list): Lista de dados do prompt.
            data_inicio (date): Data de início.
            data_fim (date): Data de fim.
            produto (int): Produto.
            df_exato (pd.DataFrame): Dataset contendo os dados exatos.
            dias (int): Dias.
        """        
        self.dataset = dataset
        self.exatos = exatos
        self.df_exato = df_exato
        self.dias = dias
        self.dados_prompt = dados_prompt

    def prompt_view(self) -> str:
        """Exibe o prompt

        Returns:
            str: Retorna o prompt
        """        
        st.write('---')
        st.write('### Prompt')
        model_prompt = PromptMercadoModels(
            dataset=self.dataset,
            exatos=self.exatos,
            dados_prompt=self.dados_prompt,
            df_exato=self.df_exato,
            dias=self.dias
        )
        result = PromptMercadoView().exibirPrompt(model_prompt)
        st.code(result, language='python',line_numbers=True)

        return result