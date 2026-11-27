import numpy as np
from openai import OpenAI
from pydantic import BaseModel

from hulp import bewaarde_vectoren, stukken

# RAG uit labo-3: zoek met embeddings het stuk dat bij
# het ticket past, en laat de LLM er een antwoord mee schrijven.
GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE)
MODEL = "gemini-3.5-flash-lite"
OLLAMA = "http://localhost:11434/v1"
embedder = OpenAI(base_url=OLLAMA, api_key="ollama")
EMBEDDING_MODEL = "embeddinggemma"
DREMPEL = 0.5

# Jouw beurt: schrijf de prompt. Zeg wat de LLM moet doen,
# zet het stuk uit de kennisbank ({stuk}) en de vraag ({vraag})
# erin, en zeg wat de LLM doet als het antwoord er niet in staat.
PROMPT = """Zeg hallo."""


# Wat de LLM schrijft.
class Antwoord(BaseModel):
    antwoord: str | None


# Wat de app voorstelt, met de bron erbij.
class Voorstel(BaseModel):
    antwoord: str | None
    bron: str | None
    score: float


def embeddings(teksten):
    antwoord = embedder.embeddings.create(model=EMBEDDING_MODEL,
                                          input=teksten)
    return [np.array(d.embedding) for d in antwoord.data]


def gelijkenis(x, y):
    return float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))


vectoren = bewaarde_vectoren(embeddings, EMBEDDING_MODEL)


def zoek(vraag):
    v = embeddings([vraag])[0]
    scores = []
    for vector in vectoren:
        scores.append(gelijkenis(vector, v))
    beste = scores.index(max(scores))
    if scores[beste] < DREMPEL:
        return None, scores[beste]
    return stukken[beste], scores[beste]


def stel_antwoord_voor(tekst):
    stuk, score = zoek(tekst)
    if stuk is None:
        return Voorstel(antwoord=None, bron=None, score=score)
    # Jouw beurt: vul het stuk en de vraag in de prompt in, en
    # vraag de LLM een Antwoord, zoals antwoord_met_rag in labo-3.
    return Voorstel(antwoord="Hallo!", bron=stuk, score=score)
