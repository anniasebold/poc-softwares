import os
from groq import Groq

PROMPT = """
Você é um assistente de turismo.
Me fale lugares turísticos em {city} - {state}.
Fale de forma clara e objetiva, com no máximo 5 frases.
Fale em forma de lista com itens numerados.
"""

def question_request(city: str, state: str) -> str | None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Please set the GROQ_API_KEY environment variable.")
        return

    client = Groq(
        api_key=api_key
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(city=city, state=state),
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content
