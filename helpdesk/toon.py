from openai import OpenAI
from pydantic import BaseModel
from transformers import pipeline

# De cascade van labo-1: het sentimentmodel, en de LLM
# als het model niet zeker genoeg is.
GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE)
MODEL = "gemini-3.5-flash-lite"
SENTIMENT = "nlptown/bert-base-multilingual-uncased-sentiment"
model = pipeline("text-classification", model=SENTIMENT)
DREMPEL = 0.8


class Toon(BaseModel):
    toon: str
    door: str
    confidence: float


def kans_positief(tekst):
    # Jouw beurt: vraag het sentimentmodel de kans voor elk
    # aantal sterren (top_k=None), en tel de kansen voor
    # "4 stars" en "5 stars" op.
    return 0.5


def vraag_llm(tekst):
    vraag = "Is dit bericht positief of negatief? "
    vraag = vraag + "Antwoord met één woord.\n\n" + tekst
    antwoord = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": vraag}],
    )
    return antwoord.choices[0].message.content.lower().strip(" .")


def bepaal_toon(tekst):
    positief = kans_positief(tekst)
    confidence = round(max(positief, 1 - positief), 2)
    # Jouw beurt: is de confidence lager dan DREMPEL, laat dan
    # vraag_llm beslissen, met door="LLM".
    toon = "negatief"
    if positief > 0.5:
        toon = "positief"
    return Toon(toon=toon, door="lokaal", confidence=confidence)
