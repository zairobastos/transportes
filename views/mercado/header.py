import streamlit as st
from datetime import date
from mercado.dado_mercado import Dados_Mercado

class DescriptionMercado:
    def __init__(self, data_inicio: date, data_fim: date, produto: int = 550):
        self.produto = produto
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def description_mercado(self):
        st.write('### Análise dos Dados')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Produto:", value=int(self.produto))
        with col2:
            st.metric(label="Data de início:", value=str(self.data_inicio))
        with col3:
            st.metric(label="Data de término:", value=str(self.data_fim))
        df_mercado, dados_prompt, dados_exatos, df_exatos = Dados_Mercado(dataset="data/sales_curva_a.csv", produto=self.produto, data_inicio=self.data_inicio, data_fim=self.data_fim).dados_prompt()
        st.write("Dataset:")
        st.dataframe(df_mercado, use_container_width=True)
        st.write("Descrição do Dataset:")
        st.dataframe(df_mercado.describe(), use_container_width=True)

        return df_mercado, dados_prompt, dados_exatos, df_exatos