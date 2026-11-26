from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from antwoord import stel_antwoord_voor
from hulp import altijd_vers
from lezen import lees_ticket
from opslag import alle_tickets, handel_af, nieuw_ticket
from toon import bepaal_toon

app = FastAPI(title="Helpdesk")


@app.get("/analyse")
def analyse(tekst: str):
    return {"toon": bepaal_toon(tekst),
            "kenmerken": lees_ticket(tekst),
            "voorstel": stel_antwoord_voor(tekst)}


class NieuwTicket(BaseModel):
    afzender: str
    tekst: str


@app.get("/tickets")
def toon_tickets():
    return alle_tickets()


@app.post("/tickets")
def maak_ticket(ticket: NieuwTicket):
    nieuw_ticket(ticket.afzender, ticket.tekst)


# Jouw beurt: POST /tickets/{id}. De pagina stuurt het bij
# Versturen en Doorsturen, met deze JSON (antwoord en voorstel
# mogen null zijn):
#   {"status": "beantwoord", "antwoord": "...", "voorstel": "..."}
# 1. Maak een Pydantic-klasse voor die JSON.
# 2. Schrijf het endpoint. Bewaar met handel_af uit opslag.py.


# Zo ziet de browser elke wijziging in web/ meteen.
altijd_vers(app)
app.mount("/", StaticFiles(directory="web", html=True))
