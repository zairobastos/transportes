from typing import Tuple
import streamlit as st
class Api:
    def run(self) -> Tuple[str, float, int]:
        """Cria a interface para configuração da API no streamlit

        Returns:
            Tuple[str, float, int]: modelo (Trata-se do modelo que o usuário selecionou), temperatura (nível de criatividade do modelo), 
            candidatos (quantidade de respostas do modelo)
        """        
        st.write('---')
        st.write('### Configurações da API')
        modelo = st.selectbox(label='Modelo', options=['gemini-1.5-pro-latest'])
        temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=1.0, step=0.05)
        candidatos = st.slider(label='Candidatos', min_value=1, max_value=10, value=1, step=1)

        return modelo, temperatura, candidatos