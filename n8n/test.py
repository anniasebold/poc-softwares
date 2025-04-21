import json
import requests
from groq_integration import question_request

def init(): 
    name = input("Digite seu nome (máximo 20 caracteres): ")
    age = input("Digite sua idade (mínimo 18 anos): ") 
    city = input("Digite a sua cidade: ")
    state = input("Digite o seu estado (em formato de sigla): ")

    if not name or not age or not city or not state:
        print("Nome, idade, cidade e estado são obrigatórios.")
        return
    
    if len(name) > 20:
        print("Nome deve ter no máximo 20 caracteres.")
        return
    
    if len(state) > 2:
        print("Estado deve ter no máximo 2 caracteres.")
        return

    if not age.isdigit() or int(age) < 18:
        print("Idade deve ser um número e maior ou igual a 18.")
        return

    if len(city) > 50:
        print("Cidade deve ter no máximo 50 caracteres.")
        return

    question_request(city, state)

def send_request(name: str, age: str):
    url = "http://localhost:5678/webhook-test/send-email"
    params = {
        "name": name,
        "age": age
    }

    try:
        response = requests.post(url, data=json.dumps(params), headers={"Content-Type": "application/json"})
        print(response)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

init()
