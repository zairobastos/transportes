import streamlit as st
from datetime import date

class Dados:
    def run(self):
        st.write('### Parâmetros da Busca')
        tipo = st.selectbox('Preveja', ['Transportes', 'Mercado'])
        st.write('### Transportes')
        linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
    
        # Convertendo data_max para um objeto date
        data_max = date(2018, 8, 1)
        data_min = date(2018, 1, 1)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        horas = st.slider(label='Horas', min_value=24, max_value=168, value=168, step=24)
        return linhas_onibus, data_inicio, data_fim, horas