from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from hulp import altijd_vers, voorbeelden
from opslag import alle_resultaten, bewaar
from stap1 import stap1
from stap2 import stap2
from stap3 import stap3

app = FastAPI(title="Mijn AI-app")


@app.get("/analyse")
def analyse(tekst: str):
    return {"stap1": stap1(tekst),
            "stap2": stap2(tekst),
            "stap3": stap3(tekst)}


class Resultaat(BaseModel):
    tekst: str
    resultaat: dict


@app.get("/voorbeelden")
def toon_voorbeelden():
    return voorbeelden


@app.get("/resultaten")
def toon_resultaten():
    return alle_resultaten()


@app.post("/resultaten")
def bewaar_resultaat(resultaat: Resultaat):
    bewaar(resultaat.tekst, resultaat.resultaat)


# Zo ziet de browser elke wijziging in web/ meteen.
altijd_vers(app)
app.mount("/", StaticFiles(directory="web", html=True))
