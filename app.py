import streamlit as st
import pandas as pd
import os
from datetime import date
from dados import Dados
from prompt import Prompt
from gemini import Gemini
import datetime
import plotly.graph_objects as go
import time


# App title
st.set_page_config(page_title="Previsão de Séries Temporais", page_icon=":bus:", layout="wide")

# Replicate Credentials
with st.sidebar:
    st.title('Previsão de Séries Temporais')
    st.write('Desenvolvido por [Zairo Bastos](https://github.com/zairobastos)')
    st.write('---')
    st.write('### Parâmetros')
    linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
    
    # Convertendo data_max para um objeto date
    data_max = date(2018, 8, 1)
    data_min = date(2018, 1, 1)
    data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
    data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))

    st.write('---')
    st.write('### Configurações Gemini')
    modelo = st.selectbox(label='Modelo', options=['gemini-1.5-pro-latest'])
    temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    candidatos = st.slider(label='Candidatos', min_value=1, max_value=10, value=1, step=1)

    confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary')


if confirma:
    st.write('### Análise de Dados')
    st.write('---')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Linha selecionada:", int(linhas_onibus))
    with col2:
        st.write("Data de início:", data_inicio)
    with col3:
        st.write("Data de término:", data_fim)
    teste = Dados('data/dados_onibus.csv', linhas_onibus, data_inicio, data_fim)
    dataset, passageiros, exatos, df_exato = teste.selecionar_dados_prompt()
    st.dataframe(dataset, use_container_width=True)

    st.write('---')
    st.write('### Prompt')
    st.write('---')
    st.write('Organização dos Dados:')
    teste2 = Prompt(dataset, passageiros, exatos, data_inicio, data_fim, linhas_onibus, df_exato)
    st.markdown(teste2.arquivos_prompt())

    st.write('---')
    st.write('### Análise de Dados')
    st.write('---')
    st.write('Primeiros 168 registros:')
    tempo = time.time()
    teste3 = Gemini(modelo, teste2.arquivos_prompt(), temperatura, candidatos)
    previsao = teste3.generate()
    tempo = time.time() - tempo
    previsao = previsao.replace('[','')
    previsao = previsao.replace(']','')
    previsao = list(map(int, previsao.split(',')))
    previsao = previsao[:168]
    st.write("Tempo de execução:", tempo)
    st.markdown(previsao)

    st.write('---')
    st.write('### Gráfico')
    st.write('---')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(exatos))), y=exatos, mode='lines', name='Valor Real'))
    fig.add_trace(go.Scatter(x=list(range(len(previsao))), y=previsao, mode='lines', name='Valor Previsto'))
    fig.update_layout(
        title=f'Passageiros por Horário / 168 horas. Série Temporal ({data_inicio} - {data_fim})',
        xaxis_title='Horário',
        yaxis_title='Passageiros',
        showlegend=True,
        colorway=['#1f77b4', '#ff7f0e'],
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


