from src.controllers.smape_controllers import SmapeController
from src.models.smape_model import SmapeModel

class SmapeView:
    @classmethod
    def executar(cls, dados: SmapeModel) -> str:
        """Executa o cálculo do erro de previsão entre os dados reais e previstos.

        Args:
            dados (SmapeModel): SmapeModel contendo os dados reais e previstos.

        Returns:
            str: Retorna o erro de previsão.
        """
        return SmapeController.calc(dados)