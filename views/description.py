import streamlit as st
from datetime import date
from transporte.dados import Dados

class Description:
    def __init__(self, data_inicio: date, data_fim: date, linhas_onibus: int = 3):
        self.linhas_onibus = linhas_onibus
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def description_transporte(self):
        st.write('### Análise dos Dados')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Linhas de ônibus", value=int(self.linhas_onibus))
        with col2:
            st.metric(label="Data de início:", value=str(self.data_inicio))
        with col3:
            st.metric(label="Data de término:", value=str(self.data_fim))
        teste = Dados('data/dados_onibus.csv', self.linhas_onibus, self.data_inicio, self.data_fim)
        dataset, passageiros, exatos, df_exato = teste.selecionar_dados_prompt()
        print(dataset)
        st.write("Dataset:")
        st.dataframe(dataset, use_container_width=True)
        st.write("Descrição do Dataset:")
        st.dataframe(dataset.describe(), use_container_width=True)

        return dataset, passageiros, exatos, df_exato
    
    def description_mercado(self):
        st.write('### Análise dos Dados')
        st.write('Em breve...')

        return None