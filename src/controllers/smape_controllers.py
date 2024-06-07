import numpy as np

from src.models.smape_model import SmapeModel

class SmapeController:
    def calc(dados: SmapeModel) -> str:
        """Calcula o erro de previsão entre os dados reais e previstos

        Args:
            dados (SmapeModel): recebe os dados reais e previstos

        Returns:
            str: retorna o erro de previsão
        """
        real = dados.real[:168]
        previsto = dados.previsto[:168]

        real, previsto = np.array(real), np.array(previsto)
        numerador = np.abs(real - previsto)
        denominador = np.abs(real) + np.abs(previsto)
        
        denominador = [denominador[i] if denominador[i]!=0 else 1 for i in range(len(denominador))]
        denominador = np.array(denominador)
        
        smape = str(round(np.mean(numerador / (denominador/2))*100, 2))+ "%"
        
        return smape