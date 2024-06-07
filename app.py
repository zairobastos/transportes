import streamlit as st
from st_pages import Page, show_pages, add_page_title
from datetime import date
import json

from src.views.description_transporte_streamlit import DescriptionTransporte
from src.views.estatisticas_transporte_streamlit import EstatisticasTransporte
from src.views.prompts_transporte_streamlit import PromptsTransporte

from src.views.description_mercado_streamlit import DescriptionMercado
from src.views.estatisticas_mercado_streamlit import EstatisticasMercado
from src.views.prompts_mercado_streamlit import PromptsMercado


from src.views.api_streamlit import Api
from src.views.grafico import Grafico
from database.crud_database import Crud


# App title
st.set_page_config(page_title="Previsão de Séries Temporais", page_icon=":bus:", layout="wide")

show_pages(
    [
        Page("app.py","Home","🏠"),
        Page("./pages/historico.py","Histórico","📜"),
    ]
)
# Replicate Credentials
with st.sidebar:
    st.write('### Parâmetros da Busca')
    tipo = st.selectbox('Preveja', ['Transportes', 'Mercado'])
    if tipo == 'Transportes':
        st.write('#### Transportes')
        linhas_onibus = st.selectbox('Linhas de ônibus', [3, 41, 42, 45, 51, 24, 76, 712, 52, 74])
        
        data_max = date(2018, 8, 1)
        data_min = date(2018, 1, 1)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 1, 1))
        
        horas = st.slider(label='Horas', min_value=24, max_value=168, value=168, step=24)

    else:
        st.write('#### Mercado')
        produto = st.selectbox('Produtos', [550, 3124, 410861, 103893, 96560, 53419, 52849, 52740, 47319, 47289])
        
        data_min = date(2017, 1, 2)
        data_max = date(2019, 4, 30)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2017, 1, 2))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2017, 1, 2))

        dias = st.slider(label='Dias', min_value=1, max_value=7, value=7, step=1)

    modelo, temperatura, candidatos = Api().run()

    confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary')


if confirma:
    if tipo == 'Transportes':
        dataset, passageiros, exatos, df_exato = DescriptionTransporte(data_inicio, data_fim, linhas_onibus).description_transporte()
        result_prompt = PromptsTransporte(dataset, passageiros, exatos, data_inicio, data_fim, linhas_onibus, df_exato, horas).prompt_view()
        previsao, hora, exato, tokens, smape = EstatisticasTransporte(modelo, result_prompt, temperatura, candidatos, horas, exatos).estatisticas()
        Grafico(previsao, hora, exato, data_inicio, data_fim, linhas_onibus, temperatura).grafico()
        data_inicio = str(data_inicio)
        data_fim = str(data_fim)

        valores_exatos_str = json.dumps(exatos)
        valores_previstos_str = json.dumps(previsao)

        Crud().insert(
            table='transporte', 
            linha=linhas_onibus, 
            data_inicio=str(data_inicio), 
            data_fim=str(data_fim), 
            horas=horas, 
            modelo=modelo, 
            temperatura=temperatura, 
            candidatos=candidatos, 
            prompt=result_prompt, 
            valores_exatos=valores_exatos_str, 
            valores_previstos=valores_previstos_str, 
            smape=smape, 
            tempo=hora, 
            tokens=tokens
        )

    else:
        df_mercado, dados_prompt, dados_exatos, df_exatos = DescriptionMercado(data_inicio, data_fim, produto).description_mercado()
        prompt = PromptsMercado(df_mercado, dados_exatos, dados_prompt, data_inicio, data_fim, produto, df_exatos, dias).prompt_view()
        previsao, hora, exato, tokens = EstatisticasMercado(modelo, prompt, temperatura, candidatos, dias, dados_exatos[:dias]).estatisticas()
        Grafico(previsao, hora, exato, data_inicio, data_fim, produto, temperatura, "").grafico()
        Crud().insert(table='mercado', produto=produto, data_inicio=data_inicio, data_fim=data_fim, dias=dias, modelo=modelo, temperatura=temperatura, candidatos=candidatos, prompt=prompt, valores_exatos=str(dados_exatos), valores_previstos=str(previsao), smape=hora, tempo=exato, tokens=tokens)
else:
    st.write('## Confirme a escolha dos parâmetros para gerar a análise.')
    st.image("icons/undraw_search_re_x5gq.svg", width=500)