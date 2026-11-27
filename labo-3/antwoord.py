from openai import OpenAI
from pydantic import BaseModel

from hulp import evalueer_antwoorden
from zoeken_embeddings import zoek_op_betekenis

GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE, max_retries=0)
MODEL = "gemini-3.5-flash-lite"

PROMPT = """Je schrijft een antwoord op de vraag van een klant
van een fietsenwinkel. Gebruik alleen de informatie
hieronder. Antwoord in de taal van de vraag, in een of
twee zinnen. Staat het antwoord er niet in, geef dan null.

Informatie: {stuk}

Vraag: {vraag}"""


class Antwoord(BaseModel):
    antwoord: str | None


def antwoord_met_rag(vraag):
    gevonden = zoek_op_betekenis(vraag)
    if gevonden["stuk"] is None:
        return {"antwoord": None, "bron": None,
                "score": gevonden["score"]}
    prompt = PROMPT.format(stuk=gevonden["stuk"], vraag=vraag)
    uitkomst = llm.chat.completions.parse(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format=Antwoord,
    )
    return {"antwoord": uitkomst.choices[0].message.parsed.antwoord,
            "bron": gevonden["stuk"],
            "score": gevonden["score"]}


evalueer_antwoorden(antwoord_met_rag)
