import pandas as pd
from src.models.mercado_prompt_model import PromptMercadoModels
from src.controllers.mercado_prompt_controller import PromptMercadoController

class PromptMercadoView:

    def exibirPrompt(self, dados: PromptMercadoModels) -> str:
        """Exibe o prompt de mercado.

        Args:
            dados (PromptMercadoModels): PromptMercadoModels contendo as informações do dataset e filtros.

        Returns:
            str: String formatada com os dias da semana e suas posições.
        """
        primeiros_dias = PromptMercadoController.primeiros_dias(dados.dataset)
        quantidade_dias = PromptMercadoController.quantidade_dias(dados.dataset)
        proximos_dias = PromptMercadoController.proximos_dias(dados.df_exato, dados.dias)
        prompt = PromptMercadoController.prompt(
            quantidade_dias=quantidade_dias, 
            primeiros_dias=primeiros_dias, 
            proximos_dias=proximos_dias,
            dados_prompt=dados.dados_prompt,
            dias=dados.dias
        )  

        return prompt