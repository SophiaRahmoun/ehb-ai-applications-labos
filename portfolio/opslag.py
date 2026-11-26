"""De databank van de app: SQLite, in het bestand app.db. Je hoeft dit bestand niet te wijzigen,
maar je mag het aanpassen voor je eigen app.

- alle_resultaten(): alles wat je bewaarde, als een lijst van dictionaries
- bewaar(tekst, resultaat): bewaart een tekst en het resultaat van /analyse
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

db = sqlite3.connect(Path(__file__).parent / "app.db", check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("""CREATE TABLE IF NOT EXISTS resultaten (
    id INTEGER PRIMARY KEY,
    tijd TEXT, tekst TEXT, resultaat TEXT)""")


def alle_resultaten():
    lijst = []
    for rij in db.execute("SELECT * FROM resultaten ORDER BY id DESC"):
        rij = dict(rij)
        rij["resultaat"] = json.loads(rij["resultaat"])
        lijst.append(rij)
    return lijst


def bewaar(tekst, resultaat):
    tijd = datetime.now().strftime("%H:%M")
    db.execute("INSERT INTO resultaten (tijd, tekst, resultaat)"
               " VALUES (?, ?, ?)", (tijd, tekst, json.dumps(resultaat)))
    db.commit()
