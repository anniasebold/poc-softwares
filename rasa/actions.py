import os
import csv
from typing import Any, Dict, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
from groq import Groq

PROMPT = """
Você é um assistente de turismo.
Me fale lugares turísticos em {city} - {state}.
Fale de forma clara e objetiva, com no máximo 5 frases.
Fale em forma de lista com itens numerados.
"""

class ValidateInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_info_form"

    def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        if len(slot_value) > 20:
            dispatcher.utter_message(text="Nome muito longo. Use até 20 caracteres.")
            return {"name": None}
        return {"name": slot_value}

    def validate_age(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        if not slot_value.isdigit() or int(slot_value) < 18:
            dispatcher.utter_message(text="Você precisa ter pelo menos 18 anos.")
            return {"age": None}
        return {"age": slot_value}

    def validate_state(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        if len(slot_value) > 2:
            dispatcher.utter_message(text="Estado inválido. Use a sigla.")
            return {"state": None}
        return {"state": slot_value}

class ActionProcessAndRespond(Action):
    def name(self) -> Text:
        return "action_process_and_respond"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> list:

        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        city = tracker.get_slot("city")
        state_sigla = tracker.get_slot("state")

        approved = int(age) >= 18

        prompt = PROMPT.format(city=city, state=state_sigla)
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        try:
            completion = llm.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"Erro ao consultar LLM: {str(e)}"
            approved = False

        # Salvar no CSV
        try:
            file_path = "respostas.csv"
            file_exists = os.path.isfile(file_path)
            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["name", "age", "city", "state", "approved", "answer_response"])
                writer.writerow([name, age, city, state_sigla, approved, response])
        except Exception as e:
            dispatcher.utter_message(text=f"Erro ao salvar CSV: {e}")
            return []

        dispatcher.utter_message(text=f"Resposta:\n{response}")
        return [SlotSet("approved", approved), SlotSet("response", response)]
