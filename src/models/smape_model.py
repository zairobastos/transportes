class SmapeModel:
    def __init__(self, real: list[int], previsto: list[int]):
        """Função de inicialização da classe SmapeModel

        Args:
            real (list[int]): lista com os dados reais
            previsto (list[int]): lista com os dados previstos
        """        
        self.real = real
        self.previsto = previsto