# De helpdesk-app

Hoe je de app ophaalt en start. De opdrachten krijg je in de les. uv, je sleutel in `.env` en Ollama installeerde je in labo 1.

---

## Ophalen

In de map van je repo. Bewaar eerst je werk:

```bash
git add .
git status
```

Staat `.env` **niet** in de lijst? Dan:

```bash
git commit -m "Labo 3"
git push
```

Open je fork op GitHub, klik **Sync fork** → **Update branch**, en dan:

```bash
git pull
uv sync
```

Ga in de terminal naar de map van de app. Zit je nog in `labo-3`, typ dan eerst `cd ..`

```bash
cd helpdesk
```

---

## Ollama

Start de Ollama-app en haal het embedding model op (621 MB):

```bash
ollama pull embeddinggemma
```

---

## De app starten

```bash
uv run fastapi dev api.py
```

Open <http://127.0.0.1:8000>. Sla je een bestand op, dan herstart de server vanzelf. Stoppen met `Ctrl+C`.

---

## Lukt het niet?

| Wat je ziet | Wat je doet |
|---|---|
| "uv wordt niet herkend" of "command not found" | sluit alle terminals (ook die in VS Code) en open een nieuwe |
| rode kronkellijnen onder een `import` in VS Code | `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`), **Python: Select Interpreter**, kies die met `.venv` erin |
| `AuthenticationError` of `401` | je sleutel ontbreekt in `.env` of klopt niet |
| `Missing credentials` | er is geen `.env`, of hij staat niet in de hoofdmap van de repo |
| `RateLimitError` of `429` | te veel vragen aan Google in één minuut: wacht een minuut |
| `503` en "high demand" | Google is druk: probeer het opnieuw |
| je wilt opnieuw beginnen met de acht tickets | stop de app, verwijder `helpdesk.db`, en start de app opnieuw |
| "Fout: kijk in de terminal van je API" | een stap loopt vast: de fout staat in de terminal waar `fastapi dev` draait |
| `Connection refused` of `could not connect` bij Ollama | start de Ollama-app, of `ollama serve` in een aparte terminal |
| `model "embeddinggemma" not found` | `ollama pull embeddinggemma` |
| "Address already in use" | `uv run fastapi dev api.py --port 8001` |

---

## Bewaren

```bash
git add .
git status
git commit -m "Helpdesk-app"
git push
```

Kijk bij `git status` of `.env` **niet** in de lijst staat.
