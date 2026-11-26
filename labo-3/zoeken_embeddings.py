import numpy as np
from openai import OpenAI

from hulp import bewaarde_vectoren, evalueer_zoeken, stukken

OLLAMA = "http://localhost:11434/v1"
embedder = OpenAI(base_url=OLLAMA, api_key="ollama")
MODEL = "embeddinggemma"
DREMPEL = 0.5


def embeddings(teksten):
    antwoord = embedder.embeddings.create(model=MODEL,
                                          input=teksten)
    return [np.array(d.embedding) for d in antwoord.data]


def gelijkenis(x, y):
    lengtes = np.linalg.norm(x) * np.linalg.norm(y)
    return float(x @ y / lengtes)


# Maak of lees de vector van elk stuk.
vectoren = bewaarde_vectoren(embeddings, MODEL)


def zoek_op_betekenis(vraag):
    # Opdracht: zoek het stuk met de grootste gelijkenis
    # met de vraag, zoals zoek_op_woorden in
    # zoeken_woorden.py. Is die gelijkenis lager dan
    # DREMPEL, dan is er geen goed stuk: geef dan None
    # als stuk. Geef een dictionary terug met "stuk" en
    # "score".
    return {"stuk": stukken[0], "score": 0.0}


evalueer_zoeken(zoek_op_betekenis)
