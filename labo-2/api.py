from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from meerdere import lees_meerdere
from regels import lees_met_regels
from structured_output import lees_met_schema
from structured_output import lees_met_schema
from meerdere import lees_meerdere

app = FastAPI()


@app.get("/regels")
def regels(tekst: str):
    return lees_met_regels(tekst)


# Opdracht: maak hier /schema, /meerdere en /ticket.
@app.get("/schema")
def schema(tekst: str):
    return lees_met_schema(tekst)


@app.get("/meerdere")
def meerdere(tekst: str):
    return lees_meerdere(tekst)


@app.get("/ticket")
def ticket(tekst: str):
    resultaat_meerdere = lees_meerdere(tekst)
    resultaat_regels = lees_met_regels(tekst)

    return {
        "categorieen": resultaat_meerdere["categorieen"],
        "taal": resultaat_regels["taal"],
        "klantnummer": resultaat_regels["klantnummer"],
        "factuurnummer": resultaat_regels["factuurnummer"]
    }


app.mount("/", StaticFiles(directory="web", html=True))
