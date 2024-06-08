import streamlit as st
import plotly.graph_objects as go
import os
from datetime import date

class Grafico:
    def __init__(self, previsao: list[int], hora:date, exatos:list[int], data_inicio:date, data_fim:date, linhas_onibus:int, temperatura:float, tipo:str = "Transportes"):
        """ Inicializa uma nova instância da classe Grafico.

        Args:
            previsao (list[int]): Previsão dos dados.
            hora (date): Hora.
            exatos (list[int]): Exatos.
            data_inicio (date): Data de início.
            data_fim (date): Data de fim.
            linhas_onibus (int): Linhas de ônibus.
            temperatura (float): Temperatura.
            tipo (str, optional): Tipo se é grafico para o transporte ou mercado. Defaults to "Transportes".
        """        
        self.previsao = previsao
        self.hora = hora
        self.exatos = exatos
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.linhas_onibus = linhas_onibus
        self.temperatura = temperatura
        self.tipo = tipo

    def grafico(self):
        """Exibe o gráfico
        """        
        st.write('---')
        st.write('### Gráfico')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(self.exatos))), y=self.exatos, mode='lines', name='Valor Real'))
        fig.add_trace(go.Scatter(x=list(range(len(self.previsao))), y=self.previsao, mode='lines', name='Valor Previsto'))
        if self.tipo == 'Transportes':
            fig.update_layout(
                title=f'Passageiros por Horário / {self.hora} horas / Série Temporal ({self.data_inicio} / {self.data_fim}) / Linha {self.linhas_onibus} / Tempratura {self.temperatura}',
                xaxis_title='Horário',
                yaxis_title='Passageiros',
                showlegend=True,
                colorway=['#1f77b4', '#ff7f0e'],
                height=600,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig.update_layout(
                title=f'Vendas por Dia / {self.hora} dias / Série Temporal ({self.data_inicio} / {self.data_fim}) / Produto {self.linhas_onibus} / Tempratura {self.temperatura}',
                xaxis_title='Dias',
                yaxis_title='Vendas',
                showlegend=True,
                colorway=['#1f77b4', '#ff7f0e'],
                height=600,
            )
            st.plotly_chart(fig, use_container_width=True)