import streamlit as st
import plotly.graph_objects as go
import os
from datetime import date

class Grafico:
    def __init__(self, previsao: list[int], hora:date, exatos:list[int], data_inicio:date, data_fim:date, linhas_onibus:int, temperatura:float):
        self.previsao = previsao
        self.hora = hora
        self.exatos = exatos
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.linhas_onibus = linhas_onibus
        self.temperatura = temperatura

    def grafico(self):
        st.write('---')
        st.write('### Gráfico')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(self.exatos))), y=self.exatos, mode='lines', name='Valor Real'))
        fig.add_trace(go.Scatter(x=list(range(len(self.previsao))), y=self.previsao, mode='lines', name='Valor Previsto'))
        fig.update_layout(
            title=f'Passageiros por Horário / {self.hora} horas / Série Temporal ({self.data_inicio} / {self.data_fim}) / Linha {self.linhas_onibus} / Tempratura {self.temperatura}',
            xaxis_title='Horário',
            yaxis_title='Passageiros',
            showlegend=True,
            colorway=['#1f77b4', '#ff7f0e'],
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

        if not os.path.exists(f'img/{self.linhas_onibus}'):
            os.makedirs(f'img/{self.linhas_onibus}')
        fig.write_image(f'img/{self.linhas_onibus}/grafico_{self.data_inicio}_{self.data_fim} {self.hora}.png', width=1400, height=600)