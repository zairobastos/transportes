import numpy as np

class Smape:
    def __init__(self, real: list[int], previsto: list[int]):
        self.real = real
        self.previsto = previsto

    def calc(self) -> float:

        real = self.real[:168]
        previsto = self.previsto[:168]

        real, previsto = np.array(real), np.array(previsto)
        numerador = np.abs(real - previsto)
        denominador = np.abs(real) + np.abs(previsto)
        
        denominador = [denominador[i] if denominador[i]!=0 else 1 for i in range(len(denominador))]
        denominador = np.array(denominador)
        
        smape = str(round(np.mean(numerador / (denominador/2))*100, 2))+ "%"
        
        return smape
