from dotenv import load_dotenv
import os
import google.generativeai as genai
import time


variables = load_dotenv()
variables = os.getenv('API_KEY')

genai.configure(api_key=variables)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)

class Gemini:
    def __init__(self, model_name, prompt, temperature, candidate_count):
        self.model_name = model_name
        self.prompt = prompt
        self.temperature = temperature
        self.candidate_count = candidate_count

    def generate(self):
        generation_config ={
            "candidate_count": self.candidate_count,
            "temperature": self.temperature,
        }
        model = genai.GenerativeModel(model_name=self.model_name)
        response = model.generate_content(self.prompt, generation_config=generation_config)
        return response.text