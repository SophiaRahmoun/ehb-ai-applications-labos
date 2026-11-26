# AI Applications: labo's

Labo's van het opleidingsonderdeel AI Applications (EhB, professionele bachelor Toegepaste Informatica).

| Labo | Onderwerp |
|---|---|
| [Labo 1](labo-1/README.md) | klantberichten indelen als positief of negatief: regels, een model van Hugging Face en een LLM, naast elkaar geëvalueerd. In les 2: een API met een webpagina, en een cascade op moeilijkere berichten |
| [Labo 2](labo-2/README.md) | helpdesktickets lezen met een LLM: een prompt die JSON vraagt, structured output met een schema (als dictionary en als Pydantic-klasse), een klein model op je eigen laptop, en zelf controleren wat het antwoordt. Thuis: meerdere categorieën per ticket, en een webapp voor de helpdesk |
| [Labo 3](labo-3/README.md) | RAG: zoeken op woorden en op betekenis met embeddings, gemeten op vragen van klanten, en een antwoord met de bron erbij |
| [Helpdesk-app](helpdesk/README.md) | de stukken van de labo's samen in één app: de toon, de velden en een voorstel van antwoord voor elk ticket |
| [Portfolio](portfolio/README.md) | het skelet voor je eigen app: een pagina, een API en drie stappen |

**Starten:** maak een fork van deze repo en volg [labo 1](labo-1/README.md): daar staat hoe je alles installeert.

**Een nieuw labo ophalen:** elke week komt er een labo bij. Open je fork op GitHub en klik op **Sync fork** → **Update branch**. Haal het daarna naar je laptop:

```bash
git pull
uv sync
```

Je eigen werk blijft staan: de nieuwe labo's komen in een nieuwe map.
