import os
import csv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from groq import Groq

PROMPT = """
Você é um assistente de turismo.
Me fale lugares turísticos em {city} - {state}.
Fale de forma clara e objetiva, com no máximo 5 frases.
Fale em forma de lista com itens numerados.
"""

class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    age: str
    city: str
    state: str
    approved: bool
    response: str

api_key = os.environ.get("GROQ_API_KEY")
llm = Groq(api_key=api_key)

# Node para coleta de dados
def input_data(state: State):
    print("=== Coleta de Dados ===")
    name = input("Digite seu nome (máximo 20 caracteres): ")
    age = input("Digite sua idade: ")
    city = input("Digite a sua cidade: ")
    state = input("Digite o seu estado (sigla): ")

    approved = True

    if not name or not age or not city or not state:
        print("Todos os campos são obrigatórios.")
        exit()

    if len(name) > 20:
        print("Nome deve ter no máximo 20 caracteres.")
        exit()

    if len(state) > 2 or len(city) > 50:
        print("Estado ou cidade excederam o tamanho permitido.")
        exit()

    if not age.isdigit() or int(age) < 18:
        approved = False

    return {
        "messages": [],
        "name": name,
        "age": age,
        "city": city,
        "state": state,
        "approved": approved,
        "response": "",
    }

# Node do Groq
def question_request(state: State):
    print("=== Consultando o LLM ===")
    prompt = PROMPT.format(city=state["city"], state=state["state"])
    chat_completion = llm.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    response = chat_completion.choices[0].message.content
    return {
        **state,
        "response": response,
        "messages": [
            AIMessage(content=response)
        ]
    }

# Node para salvar CSV
def save_to_csv(state: State):
    print("=== Salvando CSV ===")
    file_path = "respostas.csv"
    file_exists = os.path.isfile(file_path)
    is_empty = not file_exists or os.path.getsize(file_path) == 0

    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if is_empty:
                writer.writerow(["name", "age", "city", "state", "approved", "answer_response"])
            writer.writerow([
                state["name"], state["age"], state["city"], state["state"],
                state["approved"], state["response"]
            ])
        print("CSV salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("input_data", input_data)
graph_builder.add_node("question_request", question_request)
graph_builder.add_node("save_to_csv", save_to_csv)

graph_builder.add_edge(START, "input_data")
graph_builder.add_edge("input_data", "question_request")
graph_builder.add_edge("question_request", "save_to_csv")
graph_builder.add_edge("save_to_csv", END)

graph = graph_builder.compile()

try:
    filename = "graph_1.png"
    image_bytes = graph.get_graph().draw_mermaid_png()

    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"Salvo como {filename}")
except Exception as e:
    print(f"error: {e}")


final_state = graph.invoke({"response": None})
print("=== Execução do Grafo ===")
print("Resposta final:", final_state["response"])