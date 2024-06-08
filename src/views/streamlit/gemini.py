from dotenv import load_dotenv
import os
import google.generativeai as genai
import time


variables = load_dotenv()
variables = os.getenv('API_KEY')

genai.configure(api_key=variables)

class Gemini:
    def __init__(self, model_name:str, prompt:str, temperature:float, candidate_count:float):
        """Inicializa uma nova instância da classe Gemini.

        Args:
            model_name (str): Nome do modelo.
            prompt (str): Texto do prompt.
            temperature (float): Nível de criatividade do modelo.
            candidate_count (float): Quantidade de respostas do modelo.
        """        
        self.model_name = model_name
        self.prompt = prompt
        self.temperature = temperature
        self.candidate_count = candidate_count

    def generate(self)-> tuple[str, any]:
        """Gera o conteúdo.

        Returns:
            tuple[str, any]: Retorna o texto gerado e a quantidade de tokens.
        """        
        generation_config ={
            "candidate_count": self.candidate_count,
            "temperature": self.temperature,
        }
        model = genai.GenerativeModel(model_name=self.model_name)
        response = model.generate_content(self.prompt, generation_config=generation_config)
        return response.text, model.count_tokens(self.prompt)