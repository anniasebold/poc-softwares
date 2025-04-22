import csv
import json
import markdown
import os
import requests
from groq_integration import question_request

def init(): 
    name = input("Digite seu nome (máximo 20 caracteres): ")
    age = input("Digite sua idade: ")
    city = input("Digite a sua cidade: ")
    state = input("Digite o seu estado (em formato de sigla): ")
    approved = True

    if not name or not age or not city or not state:
        print("Nome, idade, cidade e estado são obrigatórios.")
        return

    if len(name) > 20:
        print("Nome deve ter no máximo 20 caracteres.")
        return

    if len(state) > 2:
        print("Estado deve ter no máximo 2 caracteres.")
        return

    if len(city) > 50:
        print("Cidade deve ter no máximo 50 caracteres.")
        return

    if not age.isdigit() or int(age) < 18:
        approved = False

    answer_response = question_request(city, state)
    response_formatted = markdown.markdown(answer_response).replace('\n', '<br>')
    send_request(name, age, approved, response_formatted)
    save_response(name, age, city, state, approved, answer_response)

def save_response(name: str, age: str, city: str, state: str, approved: bool, answer_response: str):
    if not answer_response:
        print("Houve um erro ao obter a resposta.")
        return

    file_path = "respostas.csv"
    file_exists = os.path.isfile(file_path)
    is_empty = not file_exists or os.path.getsize(file_path) == 0

    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if is_empty:
                writer.writerow(["name", "age", "city", "state", "approved", "answer_response"])

            writer.writerow([name, age, city, state, approved, answer_response])
        print("Dados salvos com sucesso em respostas.csv")
    except Exception as e:
        print(f"Erro ao salvar os dados no CSV: {e}")

def send_request(name: str, age: str, approved: bool, answer_response: str):
    url = "http://localhost:5678/webhook-test/send-email"
    params = {
        "name": name,
        "age": age,
        "approved": approved,
        "response": answer_response
    }

    try:
        response = requests.post(url, data=json.dumps(params), headers={"Content-Type": "application/json"})
        print(response)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

init()
