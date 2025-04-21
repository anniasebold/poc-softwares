import os
from groq import Groq

def question_request(city: str, state: str):
    api_key = os.getenv("GROQ_API_KEY")
    print("GROQ API Key:", api_key)
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
                "content": f"Me fale lugares turísticos em {city} - {state}.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)
