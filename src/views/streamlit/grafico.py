import streamlit as st
import plotly.graph_objects as go
import os
from datetime import date

class Grafico:
    def __init__(self, previsao: list[int], exatos:list[int], tipo:str = "Transportes"):
        """ Inicializa uma nova instância da classe Grafico.

        Args:
            previsao (list[int]): Previsão dos dados.
            exatos (list[int]): Exatos.
            tipo (str, optional): Tipo se é grafico para o transporte ou mercado. Defaults to "Transportes".
        """        
        self.previsao = previsao
        self.exatos = exatos
        self.tipo = tipo

    def grafico(self):
        """Exibe o gráfico
        """        
        st.write('### Gráfico')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(self.exatos))), y=self.exatos, mode='lines', name='Valor Real'))
        fig.add_trace(go.Scatter(x=list(range(len(self.previsao))), y=self.previsao, mode='lines', name='Valor Previsto'))
        if self.tipo == 'Transportes':
            fig.update_layout(
                title=f'Passageiros por Horário',
                xaxis_title='Horário',
                yaxis_title='Passageiros',
                showlegend=True,
                colorway=['#1f77b4', '#ff7f0e'],
                height=600,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig.update_layout(
                title=f'Vendas por Dia',
                xaxis_title='Dias',
                yaxis_title='Vendas',
                showlegend=True,
                colorway=['#1f77b4', '#ff7f0e'],
                height=600,
            )
            st.plotly_chart(fig, use_container_width=True)