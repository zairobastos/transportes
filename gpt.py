import openai
import os

# Obtém a chave da API a partir das variáveis de ambiente
key = os.getenv('KEY_GPT')

# Configura a chave da API
openai.api_key = key

# Faz uma solicitação de completude de texto usando o modelo gpt-3.5-turbo ou gpt-4
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Modelo a ser utilizado
    messages=[{"role": "user", "content": "Once upon a time"}],  # Mensagem inicial para a completude
    max_tokens=100,  # Número máximo de tokens na resposta
    temperature=1.0  # Controla a criatividade da resposta
)

# Imprime a resposta
print(response.choices[0].message['content'].strip())
