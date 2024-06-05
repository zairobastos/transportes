import streamlit as st
import time
from datetime import date, datetime
from gemini import Gemini
from smape import Smape

class Estatisticas:
    def __init__(self, modelo:str, result_prompt:str, temperatura:float, candidatos:int, horas:int, exatos:list):
        self.modelo = modelo
        self.result_prompt = result_prompt
        self.temperatura = temperatura
        self.candidatos = candidatos
        self.horas = horas
        self.exatos = exatos

    def estatisticas(self):
        st.write('---')
        st.write('### Estatística')

        tempo_inicio = time.time()
        modelo_gemini = Gemini(self.modelo, self.result_prompt, self.temperatura, self.candidatos)
        previsao_str, tokens = modelo_gemini.generate()
        tempo_execucao = time.time() - tempo_inicio
        
        previsao = [int(x.strip("] ")) for x in previsao_str.strip("[]\n").split(",")]
        previsao = previsao[:self.horas]
        exatos = self.exatos[:self.horas]
        smape = Smape(exatos, previsao).calc()
        tokens = int(str(tokens).split()[1])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Tempo de execução', value=str(round(tempo_execucao, 2))+"s")
        with col2:
            st.metric(label='Quantidade de Tokens', value=tokens)
        with col3:
            st.metric(label='SMAPE', value=smape)
        
        st.write("---")
        st.write("### Resultados")
        st.write("Lista com os dados Exatos:")
        st.code(exatos)
        st.write("Lista com os dados Previstos:")
        st.code(previsao)

        hora = datetime.now()
        return previsao, hora, exatos, tokens, smape
