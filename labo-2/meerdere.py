import json
import time

from openai import InternalServerError, RateLimitError

from hulp import lees
from structured_output import MODEL, llm

# Opdracht 1: een ticket kan over meer dan één probleem gaan.
# Schrijf hier een PROMPT en een SCHEMA, zoals in
# structured_output.py, met een veld categorieen: een lijst
# van categorieën, in de volgorde waarin ze in het ticket staan.
PROMPT = """
lees de volgende klantenticket

Geef alle categorieën die in het ticket voorkomen,
in dezelfde volgorde als de problemen in de tekst.

mogelijke categorieën:
facturatie, levering, defect, account, verhuur.

geef elke categorie maar één keer.
Gebruik het JSON Schema voor het antwoord.

Ticket:
"""


SCHEMA = {
    "type": "object",
    "properties": {
        "categorieen": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "facturatie",
                    "levering",
                    "defect",
                    "account",
                    "verhuur"
                ]
            }
        }
    },
    "required": ["categorieen"]
}


def lees_meerdere(tekst):
    # Opdracht 2: vraag het aan de LLM met jouw PROMPT en SCHEMA,
    # zoals lees_met_schema in structured_output.py.
    antwoord = llm.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": PROMPT + tekst}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ticket",
                "schema": SCHEMA
            }
        },
    )

    return json.loads(antwoord.choices[0].message.content)


def evalueer_meerdere(functie):
    # Opdracht 3: tel hoe vaak de lijst van categorieën juist is.
    # Telt de volgorde mee? Tel het op meer dan één manier.
    tickets = lees("tickets_meerdere.csv")
    for ticket in tickets:
        antwoord = functie(ticket["tekst"])
        label = ticket["categorieen"].split("|")
        print(antwoord["categorieen"], label)


if __name__ == "__main__":
    evalueer_meerdere(lees_meerdere)
