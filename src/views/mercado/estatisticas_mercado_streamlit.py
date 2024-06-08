import streamlit as st
import time
from datetime import datetime
from src.models.smape_model import SmapeModel
from src.views.streamlit.gemini import Gemini
from src.views.streamlit.smape_view import SmapeView

class EstatisticasMercado:
    def __init__(self, modelo:str, result_prompt:str, temperatura:float, candidatos:int, dias:int, exatos:list):
        """ Inicializa uma nova instância da classe Estatisticas.

        Args:
            modelo (str): Modelo que o usuário selecionou.
            result_prompt (str): Resultado do prompt.
            temperatura (float): Nível de criatividade do modelo.
            candidatos (int): Quantidade de respostas do modelo.
            dias (int): Dias.
            exatos (list): Lista de exatos.
        """        
        self.modelo = modelo
        self.result_prompt = result_prompt
        self.temperatura = temperatura
        self.candidatos = candidatos
        self.dias = dias
        self.exatos = exatos

    def estatisticas(self)-> tuple[list, datetime, list]:
        """Executa a descrição e análise dos dados de transporte.

        Returns:
            tuple[list, datetime, list]: Previsão, hora e exatos.
        """        
        st.write('---')
        st.write('### Estatística')

        tempo_inicio = time.time()
        modelo_gemini = Gemini(self.modelo, self.result_prompt, self.temperatura, self.candidatos)
        previsao_str, tokens = modelo_gemini.generate()
        tempo_execucao = time.time() - tempo_inicio
        
        previsao = [float(x.strip("] ")) for x in previsao_str.strip("[]\n").split(",")]
        previsao = previsao[:self.dias]
        exatos = self.exatos[:self.dias]
        smape_model = SmapeModel(real=exatos, previsto=previsao)
        smape = SmapeView.executar(smape_model)
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
