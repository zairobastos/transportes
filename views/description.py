import streamlit as st
from datetime import date
from src.models.transporte_dados_models import DadosTransporteModels
from src.views.transporte_dados_view import DadosTransporteView

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
        dados_transporte = DadosTransporteModels(
            dataset='data/dados_onibus.csv', 
            linhas_onibus=self.linhas_onibus, 
            data_inicio=self.data_inicio, 
            data_fim=self.data_fim
        )
        dataset, passageiros, exatos, df_exato = DadosTransporteView.executar(dados_transporte)
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