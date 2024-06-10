import streamlit as st
from database.crud_database import Crud
import pandas as pd

from src.views.streamlit.grafico import Grafico

# App title
st.write('# 📜 Histórico')

with st.sidebar:
    st.write('### Parâmetros da Busca')
    opcao = st.selectbox('Histórico', ['transporte', 'mercado'], )

    if opcao == 'transporte':
        st.write('#### Transportes')
        linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
    else:
        st.write('#### Mercado')
        produto = st.selectbox('Produtos', [550, 3124, 410861, 103893, 96560, 53419, 52849, 52740, 47319, 47289])
    smape = st.slider(label='SMAPE', min_value=0, max_value=100, value=15, step=1)
    confirmar = st.button(label='Buscar', key='buscar', help='Clique para buscar os dados',type='primary', use_container_width=True)

if confirmar:
    if opcao == 'transporte':
        transporte = Crud().select_where(table = opcao, linha = linhas_onibus, smape = smape)
        c = 1
        for row in transporte:  
            exato = list(map(int, row[9].strip('[]').split(', ')))
            previsto = list(map(int, row[10].strip('[]').split(', ')))
            Grafico(exatos=exato,previsao=previsto).grafico()

            
            st.markdown(
                """
                <style>
                .full-width-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .full-width-table th, .full-width-table td {
                    padding: 8px;
                    text-align: left;
                    font-size: 18px;
                }
                .full-width-table th {
                    text-align: center;
                    background-color: #333;
                    color: #fff;
                }
                .centered {
                    text-align: center;
                    background-color: #333;
                    color: #fff;
                    font-weight: bold;
                }
                .full-width-table tr:nth-child(even) {
                    background-color: #444;
                }
                .full-width-table tr:nth-child(odd) {
                    background-color: #666;
                }
                .full-width-table td {
                    color: #fff;
                    font-weight: bold;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <table class="full-width-table">
                    <thead>
                        <tr>
                            <th colspan="2" class="centered">Parâmetros do Prompt</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Linhas de ônibus</td>
                            <td>{int(row[1])}</td>
                        </tr>
                        <tr>
                            <td>Data de início</td>
                            <td>{str(row[2])}</td>
                        </tr>
                        <tr>
                            <td>Data de término</td>
                            <td>{str(row[3])}</td>
                        </tr>
                        <tr>
                            <td>Horas</td>
                            <td>{str(row[4])}</td>
                        </tr>
                        <tr>
                            <th colspan="2" class="centered">Parâmetros da API</th>
                        </tr>
                        <tr>
                            <td>Modelo</td>
                            <td>{str(row[5])}</td>
                        </tr>
                        <tr>
                            <td>Temperatura da Resposta</td>
                            <td>{str(row[6])}</td>
                        </tr>
                        <tr>
                            <td>Tokens</td>
                            <td>{str(row[13])}</td>
                        </tr>
                        <tr>
                            <td>Candidatos</td>
                            <td>1</td>
                        </tr>
                        <tr>
                            <th colspan="2" class="centered">Resultados da Consulta</th>
                        </tr>
                        <tr>
                            <td>SMAPE</td>
                            <td>{row[11]}</td>
                        </tr>
                        <tr>
                            <td>Valores Previstos</td>
                            <td>{row[10]}</td>
                        </tr>
                    </tbody>
                </table>
                """,
                unsafe_allow_html=True
            )
            st.write("### Prompt")
            st.code(row[8])
            c+=1
            st.write('---')
    else:
        varejo = Crud().select_where(table = opcao, produto = produto, smape = smape)
        c = 1
        for row in varejo:  
            exato = list(map(float, row[9].strip('[]').split(', ')))
            previsto = list(map(float, row[10].strip('[]').split(', ')))
            Grafico(exatos=exato,previsao=previsto).grafico()

            st.markdown(
                """
                <style>
                .full-width-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .full-width-table th, .full-width-table td {
                    padding: 8px;
                    text-align: left;
                    font-size: 18px;
                }
                .full-width-table th {
                    text-align: center;
                    background-color: #333;
                    color: #fff;
                }
                .centered {
                    text-align: center;
                    background-color: #333;
                    color: #fff;
                    font-weight: bold;
                }
                .full-width-table tr:nth-child(even) {
                    background-color: #444;
                }
                .full-width-table tr:nth-child(odd) {
                    background-color: #666;
                }
                .full-width-table td {
                    color: #fff;
                    font-weight: bold;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <table class="full-width-table">
                    <thead>
                        <tr>
                            <th colspan="2" class="centered">Parâmetros do Prompt</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Produto</td>
                            <td>{int(row[1])}</td>
                        </tr>
                        <tr>
                            <td>Data de início</td>
                            <td>{str(row[2])}</td>
                        </tr>
                        <tr>
                            <td>Data de término</td>
                            <td>{str(row[3])}</td>
                        </tr>
                        <tr>
                            <td>Dias</td>
                            <td>{str(row[4])}</td>
                        </tr>
                        <tr>
                            <th colspan="2" class="centered">Parâmetros da API</th>
                        </tr>
                        <tr>
                            <td>Modelo</td>
                            <td>{str(row[5])}</td>
                        </tr>
                        <tr>
                            <td>Temperatura da Resposta</td>
                            <td>{str(row[6])}</td>
                        </tr>
                        <tr>
                            <td>Tokens</td>
                            <td>{str(row[13])}</td>
                        </tr>
                        <tr>
                            <td>Candidatos</td>
                            <td>1</td>
                        </tr>
                        <tr>
                            <th colspan="2" class="centered">Resultados da Consulta</th>
                        </tr>
                        <tr>
                            <td>SMAPE</td>
                            <td>{row[11]}</td>
                        </tr>
                        <tr>
                            <td>Valores Previstos</td>
                            <td>{row[10]}</td>
                        </tr>
                    </tbody>
                </table>
                """,
                unsafe_allow_html=True
            )
            st.write("### Prompt")
            st.code(row[8])
            c+=1
            st.write('---')