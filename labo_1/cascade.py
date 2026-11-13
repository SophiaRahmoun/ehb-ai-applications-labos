from .hulp import evalueer
from .lokaal import model
from .taalmodel import voorspel_met_taalmodel

DREMPEL = 0.8


#def lokaal_met_confidence(tekst):
    # Opdracht: vraag het sentimentmodel om alle vijf de kansen.
    # Geef het antwoord van lokaal.py terug, en hoe zeker het daarvan is.
   # return "positief", 1.0


#def voorspel_met_cascade(tekst):
    # Opdracht: vraag het eerst aan het sentimentmodel.
    # Is de confidence lager dan DREMPEL? Vraag het dan aan de LLM.
   # return "positief"



#todo: functies schrijven in cascade.py: lokaal_met_confidence en voorspel_met_cascade

def lokaal_met_confidence(tekst):
    resultaat = model(tekst, top_k=5)
    positief = 0

    for item in resultaat:
        if item["label"] in ["4 stars", "5 stars"]:
            positief += item["score"]

    if positief >= 0.5:
        return "positief", round(positief, 2)

    return "negatief", round(1 - positief, 2)


def voorspel_met_cascade(tekst):
   
    sentiment, confidence = lokaal_met_confidence(tekst)
    if confidence < DREMPEL:
        sentiment = voorspel_met_taalmodel(tekst)
        door = "LLM"
    else:
        door = "lokaal"
    return {"sentiment": sentiment, "door": door, "confidence": confidence}


evalueer(voorspel_met_cascade, "moeilijke_berichten.csv")
