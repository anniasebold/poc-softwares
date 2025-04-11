import json
import requests

def init(): 
    name = input("Digite seu nome (máximo 20 caracteres): ")
    
    if len(name) > 20:
        print("Nome deve ter no máximo 20 caracteres.")
        return

    age = input("Digite sua idade (mínimo 18 anos): ")

    if not name or not age:
        print("Nome e idade são obrigatórios.")
        return

    send_request(name, age)

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
