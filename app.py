import streamlit as st
from datetime import date
from views.description import Description
from views.estatisticas import Estatisticas
from views.grafico import Grafico
from views.prompts import Prompts
from views.api import Api


# App title
st.set_page_config(page_title="Previsão de Séries Temporais", page_icon=":bus:", layout="wide")

# Replicate Credentials
with st.sidebar:
    st.write('### Parâmetros da Busca')
    tipo = st.selectbox('Preveja', ['Transportes', 'Mercado'])
    if tipo == 'Transportes':
        st.write('### Transportes')
        linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
    
        # Convertendo data_max para um objeto date
        data_max = date(2018, 8, 1)
        data_min = date(2018, 1, 1)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        horas = st.slider(label='Horas', min_value=24, max_value=168, value=168, step=24)
    else:
        st.write('### Mercado')
        st.write('Em breve...')

    modelo, temperatura, candidatos = Api().run()

    confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary')


if confirma:
    dataset, passageiros, exatos, df_exato = Description(data_inicio, data_fim,linhas_onibus).description_transporte()
    result_prompt = Prompts(dataset, passageiros, exatos, data_inicio, data_fim, linhas_onibus, df_exato, horas).prompt_view()
    previsao, hora, exato = Estatisticas(modelo, result_prompt, temperatura, candidatos, horas, exatos).estatisticas()
    Grafico(previsao, hora, exato, data_inicio, data_fim, linhas_onibus, temperatura).grafico()
    
else:
    st.write('## Confirme a escolha dos parâmetros para gerar a análise.')
    st.image("icons/undraw_search_re_x5gq.svg", width=500)


