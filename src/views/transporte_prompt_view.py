import pandas as pd
from src.models.transporte_dados_models import DadosTransporteModels
from src.controllers.transporte_prompt_controller import PromptTransporteController


class PromptTransporteView:

    def exibirPrompt(self, dados: DadosTransporteModels):
        """Exibe o prompt de transporte.

        Args:
            dados (DadosTransporteModels): DadosTransporteModels contendo as informações do dataset e filtros.

        Returns:
            str: String formatada com os dias da semana e suas posições.
        """
        primeiros_dias = PromptTransporteController.primeiros_dias(dados.dataset)
        feriados = PromptTransporteController.feriados(dados.dataset)
        proximos_dias = PromptTransporteController.proximos_dias(dados.dataset)
        quantidade_dias = PromptTransporteController.quantidade_dias(dados.dataset)
        prompt = PromptTransporteController.prompt(
            quantidade_dias=quantidade_dias, 
            primeiros_dias=primeiros_dias, 
            feriados=feriados, 
            proximos_dias=proximos_dias,
            dados_prompt= dados.dados_prompt,
            horas=dados.horas
        )  

        return prompt  