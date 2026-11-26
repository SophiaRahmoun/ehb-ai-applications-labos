"""Hulp bij je app. Je hoeft dit bestand niet te wijzigen.

- leest je sleutel uit het bestand .env in de hoofdmap van de repo
- voorbeelden: de regels uit voorbeelden.csv, als een lijst van dictionaries. De pagina
  toont ze, en evalueer meet erop
- probeer(functie): stuurt elke tekst uit voorbeelden.csv naar je functie en toont wat
  ze teruggeeft
- evalueer(functie, veld): vergelijkt per voorbeeld het veld uit je dictionary met de
  kolom met dezelfde naam in voorbeelden.csv, en toont hoeveel er juist zijn en hoe lang
  je functie erover deed
- voor RAG, zoals in labo 3: stukken (de alinea's van de documenten in de map
  kennisbank, als die er is), naam(stuk), en bewaarde_vectoren(embeddings, model)
"""

import csv
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

MAP = Path(__file__).parent
load_dotenv(MAP.parent / ".env")

console = Console()

with open(MAP / "voorbeelden.csv", encoding="utf-8-sig", newline="") as bestand:
    voorbeelden = list(csv.DictReader(bestand))

# Lees elk document in kennisbank en knip het op bij elke lege regel.
stukken = []
namen = []
for document in sorted((MAP / "kennisbank").glob("*.md")):
    alineas = document.read_text(encoding="utf-8").strip().split("\n\n")
    for nummer, alinea in enumerate(alineas, start=1):
        stukken.append(alinea.strip())
        namen.append(f"{document.name}#{nummer}")


def naam(stuk):
    """Waar een stuk vandaan komt, zoals "verhuur.md#2"."""
    if stuk in stukken:
        return namen[stukken.index(stuk)]
    return None


def bewaarde_vectoren(embeddings, model):
    """Een vector voor elk stuk: uit het bestand als dat er al is, anders van embeddings(stukken)."""
    bestand = MAP / "vectoren" / (model.replace(":", "-").replace("/", "-") + ".npz")
    if bestand.exists():
        bewaard = np.load(bestand)
        if list(bewaard["stukken"]) == stukken:
            return bewaard["vectoren"]
    vectoren = np.array(embeddings(stukken))
    bestand.parent.mkdir(exist_ok=True)
    np.savez(bestand, vectoren=vectoren, stukken=np.array(stukken))
    console.print(f"[dim]{len(stukken)} vectoren gemaakt met {model}, bewaard in vectoren/{bestand.name}[/]")
    return vectoren


def als_tekst(waarde):
    if waarde is None:
        return ""
    if isinstance(waarde, float):
        return str(round(waarde, 2))
    if waarde in stukken:
        return naam(waarde)
    return str(waarde).strip()


def probeer(functie):
    """Stuurt elke tekst uit voorbeelden.csv naar functie(tekst) en toont wat ze teruggeeft."""
    if functie.__module__ != "__main__":
        return  # api.py gebruikt je functie: dan proberen we niets

    tabel = Table(title=f"{functie.__name__} op voorbeelden.csv", title_justify="left", show_lines=True)
    tabel.add_column("tekst", max_width=40)
    tabel.add_column("antwoord van je functie")
    for voorbeeld in voorbeelden:
        uitkomst = functie(voorbeeld["tekst"])
        if uitkomst is None:
            tekst = "[yellow]None: nog niet gemaakt[/]"
        elif isinstance(uitkomst, dict):
            tekst = "\n".join(f"{sleutel}: {als_tekst(uitkomst[sleutel])}" for sleutel in uitkomst)
        else:
            tekst = f"[red]geen dictionary maar {type(uitkomst).__name__}[/]"
        tabel.add_row(voorbeeld["tekst"], tekst)
    console.print(tabel)


def evalueer(functie, veld):
    """Vergelijkt functie(tekst)[veld] met de kolom veld in voorbeelden.csv. Lege labels tellen niet mee."""
    if functie.__module__ != "__main__":
        return
    if veld not in voorbeelden[0]:
        console.print(f"[red]voorbeelden.csv heeft geen kolom {veld}[/]")
        return

    juist = 0
    gemeten = 0
    start = time.perf_counter()
    for voorbeeld in voorbeelden:
        if not voorbeeld[veld]:
            continue
        uitkomst = functie(voorbeeld["tekst"])
        gemeten = gemeten + 1
        if isinstance(uitkomst, dict) and als_tekst(uitkomst.get(veld)).lower() == voorbeeld[veld].strip().lower():
            juist = juist + 1
    if gemeten == 0:
        console.print(f"[yellow]nog geen labels in de kolom {veld}[/]")
        return
    seconden = (time.perf_counter() - start) / gemeten
    console.print(f"[bold]{veld}: {juist}/{gemeten} juist[/] · {seconden:.2f} seconden per voorbeeld")


def altijd_vers(app):
    """Laat de browser bij elke keer laden nakijken of een bestand veranderd is."""
    @app.middleware("http")
    async def geen_cache(request, call_next):
        antwoord = await call_next(request)
        antwoord.headers["Cache-Control"] = "no-cache"
        return antwoord
