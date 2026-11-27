"""De databank van de app: SQLite, in het bestand helpdesk.db. Je hoeft dit bestand niet te wijzigen.

- alle_tickets(): alle tickets, als een lijst van dictionaries
- nieuw_ticket(afzender, tekst): bewaart een nieuw ticket
- handel_af(id, status, antwoord, voorstel): bewaart wat de medewerker met een ticket deed

De eerste keer zet het de tickets uit voorbeelden.csv in de databank.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from hulp import voorbeelden

db = sqlite3.connect(Path(__file__).parent / "helpdesk.db", check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("""CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    afzender TEXT, tijd TEXT, tekst TEXT,
    status TEXT, antwoord TEXT, voorstel TEXT)""")


def alle_tickets():
    rijen = db.execute("SELECT * FROM tickets ORDER BY id DESC")
    return [dict(rij) for rij in rijen]


def nieuw_ticket(afzender, tekst, tijd=None):
    tijd = tijd or datetime.now().strftime("%H:%M")
    db.execute("INSERT INTO tickets (afzender, tijd, tekst) VALUES (?, ?, ?)",
               (afzender, tijd, tekst))
    db.commit()


def handel_af(id, status, antwoord, voorstel):
    db.execute("UPDATE tickets SET status = ?, antwoord = ?, voorstel = ?"
               " WHERE id = ?", (status, antwoord, voorstel, id))
    db.commit()


if not alle_tickets():
    for voorbeeld in voorbeelden:
        nieuw_ticket(voorbeeld["afzender"], voorbeeld["tekst"], voorbeeld["tijd"])
