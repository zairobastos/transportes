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
import datetime
import numpy as np

def smape(a, f):
    print(a)
    print(f)

    return 1/len(a) * np.sum(np.abs(f-a) / (np.abs(a) + np.abs(f))/2)


# App title
st.set_page_config(page_title="Previsão de Séries Temporais", page_icon=":bus:", layout="wide")

# Replicate Credentials
with st.sidebar:
    st.write('### Parâmetros da Busca')
    linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
    
    # Convertendo data_max para um objeto date
    data_max = date(2018, 8, 1)
    data_min = date(2018, 1, 1)
    data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
    data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
    horas = st.slider(label='Horas', min_value=24, max_value=168, value=168, step=24)

    st.write('---')
    st.write('### Configurações da API')
    modelo = st.selectbox(label='Modelo', options=['gemini-1.5-pro-latest'])
    temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    candidatos = st.slider(label='Candidatos', min_value=1, max_value=10, value=1, step=1)

    confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary')


if confirma:
    st.write('### Análise dos Dados')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Linha selecionada:", int(linhas_onibus))
    with col2:
        st.write("Data de início:", data_inicio)
    with col3:
        st.write("Data de término:", data_fim)
    teste = Dados('data/dados_onibus.csv', linhas_onibus, data_inicio, data_fim)
    dataset, passageiros, exatos, df_exato = teste.selecionar_dados_prompt()
    st.write("Dataset:")
    st.dataframe(dataset, use_container_width=True)
    st.write("Descrição do Dataset:")
    st.dataframe(dataset.describe(), use_container_width=True)

    st.write('---')
    st.write('### Prompt')
    teste2 = Prompt(dataset, passageiros, exatos, data_inicio, data_fim, linhas_onibus, df_exato[:horas], horas)
    st.code(teste2.arquivos_prompt())

    st.write('---')
    st.write('### Dados previstos')
    tempo = time.time()
    teste3 = Gemini(modelo, teste2.arquivos_prompt(), temperatura, candidatos)
    previsao, tokens = teste3.generate()
    tempo = time.time() - tempo
    previsao = previsao.replace('[','')
    previsao = previsao.replace(']','')
    previsao = list(map(int, previsao.split(',')))
    previsao = previsao[:horas]
    exatos = exatos[:horas]
    st.write("Tempo de execução:", tempo)
    st.write(tokens)
    st.write("SMAPE:", smape(np.array(exatos),np.array(previsao)))
    st.write("Exatos:")
    st.markdown(exatos)
    st.write("Previsão:")
    st.markdown(previsao)
    hora = datetime.datetime.now()

    st.write('---')
    st.write('### Gráfico')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(exatos))), y=exatos, mode='lines', name='Valor Real'))
    fig.add_trace(go.Scatter(x=list(range(len(previsao))), y=previsao, mode='lines', name='Valor Previsto'))
    fig.update_layout(
        title=f'Passageiros por Horário / {horas} horas / Série Temporal ({data_inicio} / {data_fim}) / Linha {linhas_onibus} / Tempratura {temperatura}',
        xaxis_title='Horário',
        yaxis_title='Passageiros',
        showlegend=True,
        colorway=['#1f77b4', '#ff7f0e'],
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)

    if not os.path.exists(f'img/{linhas_onibus}'):
        os.makedirs(f'img/{linhas_onibus}')
    fig.write_image(f'img/{linhas_onibus}/grafico_{data_inicio}_{data_fim} {hora}.png', width=1400, height=600)
    


