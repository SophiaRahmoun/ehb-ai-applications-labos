# Labo 3: RAG

Hoe je de bestanden ophaalt en de scripts start. De opdrachten krijg je in de les. uv, je sleutel in `.env` en Ollama installeerde je in labo 1.

---

## Je werk bewaren en labo 3 ophalen

In de map van je repo. Bewaar eerst je werk:

```bash
git add .
git status
```

Staat `.env` **niet** in de lijst? Dan:

```bash
git commit -m "Labo 2"
git push
```

Open je fork op GitHub, klik **Sync fork** → **Update branch**, en dan:

```bash
git pull
uv sync
```

Ga in de terminal naar de map van dit labo. Zit je nog in `labo-2`, typ dan eerst `cd ..`

```bash
cd labo-3
```

---

## Ollama

Start de Ollama-app en haal het embedding model op (621 MB):

```bash
ollama pull embeddinggemma
```

---

## De scripts starten

In de map van dit labo:

```bash
uv run rag_intro.py
uv run zoeken_woorden.py
uv run zoeken_embeddings.py
uv run antwoord.py
```

---

## Lukt het niet?

| Wat je ziet | Wat je doet |
|---|---|
| "uv wordt niet herkend" of "command not found" | sluit alle terminals (ook die in VS Code) en open een nieuwe |
| rode kronkellijnen onder een `import` in VS Code | `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`), **Python: Select Interpreter**, kies die met `.venv` erin |
| `AuthenticationError` of `401` | je sleutel ontbreekt in `.env` of klopt niet |
| `Missing credentials` | er is geen `.env`, of hij staat niet in de hoofdmap van de repo |
| "Google antwoordt 429" of "Google antwoordt 503: 20 seconden wachten" | de rate limit, of Google is druk: het script wacht en probeert opnieuw |
| `Connection refused` of `could not connect` bij Ollama | start de Ollama-app, of `ollama serve` in een aparte terminal |
| `model "embeddinggemma" not found` | `ollama pull embeddinggemma` |
| de tabel is te breed voor je terminal | maak het venster breder, of sleep het terminalpaneel in VS Code naar boven |

---

## Bewaren

```bash
git add .
git status
git commit -m "Labo 3"
git push
```

Kijk bij `git status` of `.env` **niet** in de lijst staat.
