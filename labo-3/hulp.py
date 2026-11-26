"""Hulp bij labo 3. Je hoeft dit bestand niet te wijzigen.

- leest je sleutel uit het bestand .env in de hoofdmap van de repo
- stukken: de alinea's van alle documenten in de map kennisbank, als een lijst van teksten
- naam(stuk): waar een stuk vandaan komt, zoals "verhuur.md#2" (de tweede alinea van verhuur.md)
- bewaarde_vectoren(embeddings, model): een vector voor elk stuk. De eerste keer maakt jouw functie
  embeddings ze, en worden ze bewaard in de map vectoren. Daarna komen ze uit dat bestand, zolang het
  model en de kennisbank niet veranderen. Zo vraag je ze niet bij elke start opnieuw aan Google.
- evalueer_zoeken(functie): test jouw zoekfunctie op de vragen in vragen.csv.
  Je functie krijgt een vraag en geeft een dictionary terug: {"stuk": ..., "score": ...},
  met None als stuk als er geen goed stuk is. Juist is: het stuk uit de labels, of niets
  bij een vraag waarop de kennisbank geen antwoord heeft.
- evalueer_antwoorden(functie): test jouw antwoordfunctie op dezelfde vragen.
  Je functie geeft een dictionary terug met minstens "antwoord": een tekst, of None als
  de vraag naar een medewerker gaat. Een antwoord is juist als het feit uit de labels
  erin staat (bv. "200" voor de waarborg van een bakfiets). Voor een vraag waarop de
  kennisbank geen antwoord heeft, is doorsturen naar een medewerker juist.
"""

import csv
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import InternalServerError, RateLimitError
from rich.console import Console
from rich.table import Table
from rich.text import Text

MAP = Path(__file__).parent
load_dotenv(MAP.parent / ".env")

console = Console()

# Lees elk document in kennisbank en knip het op bij elke lege regel.
stukken = []
namen = []
for bestand in sorted((MAP / "kennisbank").glob("*.md")):
    alineas = bestand.read_text(encoding="utf-8").strip().split("\n\n")
    for nummer, alinea in enumerate(alineas, start=1):
        stukken.append(alinea.strip())
        namen.append(f"{bestand.name}#{nummer}")


def naam(stuk):
    """Waar een stuk vandaan komt, zoals "verhuur.md#2"."""
    if stuk in stukken:
        return namen[stukken.index(stuk)]
    return "geen stuk uit de kennisbank"


def bewaarde_vectoren(embeddings, model):
    """Een vector voor elk stuk: uit het bestand als dat er al is, anders van embeddings(stukken)."""
    bestand = MAP / "vectoren" / (model.replace(":", "-").replace("/", "-") + ".npz")
    if bestand.exists():
        bewaard = np.load(bestand)
        if list(bewaard["stukken"]) == stukken:
            return bewaard["vectoren"]
    vectoren = np.array(vraag_met_geduld(embeddings, stukken))
    bestand.parent.mkdir(exist_ok=True)
    np.savez(bestand, vectoren=vectoren, stukken=np.array(stukken))
    console.print(f"[dim]{len(stukken)} vectoren gemaakt met {model}, bewaard in vectoren/{bestand.name}[/]")
    return vectoren


def lees(bestand="vragen.csv"):
    with open(MAP / bestand, encoding="utf-8-sig", newline="") as csv_bestand:
        return list(csv.DictReader(csv_bestand))


def vraag_met_geduld(functie, vraag):
    """Antwoordt Google met 429 (te veel vragen per minuut) of 503 (te druk), dan wachten we en proberen opnieuw."""
    for poging in range(5):
        try:
            return functie(vraag)
        except (RateLimitError, InternalServerError) as fout:
            console.print(f"  [yellow]Google antwoordt {fout.status_code}: 20 seconden wachten[/]")
            time.sleep(20)
    return functie(vraag)


def kort(tekst, lengte=70):
    tekst = " ".join(str(tekst).split())
    if len(tekst) > lengte:
        return tekst[:lengte] + "…"
    return tekst


def evalueer_zoeken(functie, bestand="vragen.csv"):
    """Test functie(vraag) op de vragen: welk stuk vindt ze, en is het het juiste?"""
    if functie.__module__ != "__main__":
        return  # een ander bestand (zoals api.py) gebruikt jouw functie: dan evalueren we niet

    import psutil

    vragen = lees(bestand)
    tabel = Table(title=f"{functie.__name__} op {bestand}", title_justify="left", show_lines=True)
    tabel.add_column("vraag", max_width=60)
    tabel.add_column("verwacht")
    tabel.add_column("gevonden")
    tabel.add_column("score", justify="right")
    juist = 0
    start = time.perf_counter()
    start_cpu = time.process_time()
    for rij in vragen:
        gevonden = vraag_met_geduld(functie, rij["vraag"])
        stuk = gevonden["stuk"]
        score = f"{gevonden['score']:.2f}" if isinstance(gevonden["score"], float) else str(gevonden["score"])
        wat = "niets gevonden" if stuk is None else naam(stuk)
        if rij["bron"]:
            goed = stuk is not None and naam(stuk) == rij["bron"]
            verwacht = rij["bron"]
        else:
            goed = stuk is None
            verwacht = "niets gevonden"
        if goed:
            juist = juist + 1
            cel = Text(f"{wat} ✓", style="green")
        else:
            cel = Text(f"{wat} ✗", style="red")
        tabel.add_row(rij["vraag"], verwacht, cel, score)
    seconden = (time.perf_counter() - start) / len(vragen)
    cpu_tijd = (time.process_time() - start_cpu) / len(vragen)
    geheugen = psutil.Process().memory_info().rss / 1_000_000
    console.print(tabel)
    console.print(f"[bold]{juist}/{len(vragen)} juist[/]")
    console.print(f"{seconden:.3f} seconden per vraag")
    console.print(f"op je eigen laptop: {cpu_tijd:.3f} seconden CPU-tijd per vraag, {geheugen:.0f} MB geheugen")


def evalueer_antwoorden(functie, bestand="vragen.csv"):
    """Test functie(vraag) op de vragen: staat het feit in het antwoord, of ging de vraag naar een medewerker?"""
    if functie.__module__ != "__main__":
        return

    import psutil

    vragen = lees(bestand)
    tabel = Table(title=f"{functie.__name__} op {bestand}", title_justify="left", show_lines=True)
    tabel.add_column("vraag", max_width=60)
    tabel.add_column("verwacht")
    tabel.add_column("antwoord", max_width=52)
    tabel.add_column("score", justify="right")
    tellers = {"juist": 0, "fout": 0, "doorgestuurd": 0, "terecht doorgestuurd": 0, "toch beantwoord": 0}
    start = time.perf_counter()
    start_cpu = time.process_time()
    for rij in vragen:
        uitkomst = vraag_met_geduld(functie, rij["vraag"])
        antwoord = uitkomst["antwoord"]
        score = uitkomst.get("score", "")
        score = f"{score:.2f}" if isinstance(score, float) else str(score)
        if rij["bron"]:
            verwacht = rij["feit"]
        else:
            verwacht = "naar een medewerker"
        if rij["bron"] and antwoord is None:
            tellers["doorgestuurd"] += 1
            cel = Text("naar een medewerker ✗", style="yellow")
        elif rij["bron"] and rij["feit"].lower() in antwoord.lower():
            tellers["juist"] += 1
            cel = Text(f"{kort(antwoord, 48)} ✓", style="green")
        elif rij["bron"]:
            tellers["fout"] += 1
            cel = Text(f"{kort(antwoord, 48)} ✗", style="red")
        elif antwoord is None:
            tellers["terecht doorgestuurd"] += 1
            cel = Text("naar een medewerker ✓", style="green")
        else:
            tellers["toch beantwoord"] += 1
            cel = Text(f"{kort(antwoord, 48)} ✗", style="red")
        tabel.add_row(rij["vraag"], verwacht, cel, score)
    seconden = (time.perf_counter() - start) / len(vragen)
    cpu_tijd = (time.process_time() - start_cpu) / len(vragen)
    geheugen = psutil.Process().memory_info().rss / 1_000_000
    console.print(tabel)
    juist = tellers["juist"] + tellers["terecht doorgestuurd"]
    console.print(f"[bold]{juist}/{len(vragen)} juist[/]")
    console.print(f"{seconden:.3f} seconden per vraag")
    console.print(f"op je eigen laptop: {cpu_tijd:.3f} seconden CPU-tijd per vraag, {geheugen:.0f} MB geheugen")
