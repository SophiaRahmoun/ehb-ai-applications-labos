import json
import time

from openai import InternalServerError, OpenAI, RateLimitError

from hulp import evalueer

GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE, max_retries=0)
#MODEL = "gemini-3.5-flash-lite"
MODEL = "gemma-4-26b-a4b-it"

PROMPT = """Lees dit helpdeskticket.
Geef JSON met deze velden:
- categorie: facturatie, levering, defect, account of verhuur
- taal: nl of fr
- klantnummer: zoals K12345, of null
- factuurnummer: zoals F2026-1234, of null

Ticket: """


def lees_met_prompt(tekst):
    try:
        antwoord = llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT + tekst}],
        )
    except (RateLimitError, InternalServerError):
        print("  Google antwoordt niet: 20 seconden wachten")
        time.sleep(20)
        return lees_met_prompt(tekst)
   
    inhoud = antwoord.choices[0].message.content
    inhoud = inhoud.strip()

    if inhoud.startswith("```json"):
        inhoud = inhoud[7:]
    elif inhoud.startswith("```"):
        inhoud = inhoud[3:]

    if inhoud.endswith("```"):
        inhoud = inhoud[:-3]

    return json.loads(inhoud.strip())

evalueer(lees_met_prompt)
