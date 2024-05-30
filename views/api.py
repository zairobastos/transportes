import streamlit as st
class Api:
    def run(self):
        st.write('---')
        st.write('### Configurações da API')
        modelo = st.selectbox(label='Modelo', options=['gemini-1.5-pro-latest'])
        temperatura = st.slider(label='Temperatura', min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        candidatos = st.slider(label='Candidatos', min_value=1, max_value=10, value=1, step=1)

        return modelo, temperatura, candidatos