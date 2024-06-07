from typing import Optional, Tuple
import pandas as pd
import streamlit as st
from datetime import date
from src.models.mercado_dados_models import DadosMercadoModels
from src.views.mercado_dados_views import DadosMercadoView

class DescriptionMercado:
    def __init__(self, data_inicio: date, data_fim: date, produto: int = 550):
        """ Inicializa uma nova instância da classe DescriptionMercado.

        Args:
            data_inicio (date): Data de início da análise
            data_fim (date): Data de término da análise
            produto (int, optional): Código do produto a ser analisado. Defaults to 550.
        """        
        self.produto = produto
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def description_mercado(self) -> Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]:
        """Executa a descrição e análise dos dados de mercado.

        Returns:
            Tuple[Optional[pd.DataFrame], Optional[list], Optional[list], Optional[pd.DataFrame]]: Dataframe com os dados do prompt, 
            dados do prompt, dados exatos e dataframe com os dados exatos. 
        """        
        st.write('### Análise dos Dados')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Produto:", value=int(self.produto))
        with col2:
            st.metric(label="Data de início:", value=str(self.data_inicio))
        with col3:
            st.metric(label="Data de término:", value=str(self.data_fim))
        dados_mercado = DadosMercadoModels(
            dataset='data/sales_curva_a.csv', 
            data_inicio=self.data_inicio, 
            data_fim=self.data_fim,
            produto=self.produto
        )
        df_mercado, dados_prompt, dados_exatos, df_exatos = DadosMercadoView.executar(dados_mercado)
        st.write("Dataset:")
        st.dataframe(df_mercado, use_container_width=True)
        st.write("Descrição do Dataset:")
        st.dataframe(df_mercado.describe(), use_container_width=True)

        return df_mercado, dados_prompt, dados_exatos, df_exatos