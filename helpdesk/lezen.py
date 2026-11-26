import re
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

# Per veld gekozen, zoals in labo-2: de LLM leest categorie
# en taal met een schema, regels lezen de nummers.
GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE)
MODEL = "gemini-3.5-flash-lite"


# Wat de LLM leest, met een schema.
# Jouw beurt: alleen de vijf categorieën zijn toegelaten
# (facturatie, levering, defect, account, verhuur). Voeg ook
# taal toe: nl of fr.
class Indeling(BaseModel):
    categorie: str


# Wat de app over een ticket te weten komt.
class Kenmerken(BaseModel):
    categorie: str | None
    taal: str | None
    klantnummer: str | None
    factuurnummer: str | None


def zoek(patroon, tekst):
    gevonden = re.search(patroon, tekst)
    if gevonden:
        return gevonden.group()
    return None


def lees_ticket(tekst):
    # Jouw beurt:
    # 1. Laat de LLM het ticket lezen in de vorm van Indeling,
    #    met llm.chat.completions.parse, zoals in labo-2.
    # 2. Lees de nummers met zoek (klantnummer: K12345,
    #    factuurnummer: F2026-1234).
    # 3. Geef Kenmerken terug.
    return Kenmerken(categorie=None, taal=None,
                     klantnummer=None, factuurnummer=None)
