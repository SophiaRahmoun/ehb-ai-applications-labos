import re

from openai import OpenAI

from hulp import stukken

GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE)
MODEL = "gemini-3.5-flash-lite"


def woorden(tekst):
    return set(re.findall(r"\w{4,}", tekst.lower()))


def overlap(vraag, stuk):
    return len(woorden(vraag) & woorden(stuk))


def zoek(vraag):
    beste = stukken[0]
    for stuk in stukken:
        if overlap(vraag, stuk) > overlap(vraag, beste):
            beste = stuk
    return beste


def vraag_llm(prompt):
    antwoord = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return antwoord.choices[0].message.content


def antwoord_met_rag(vraag):
    stuk = zoek(vraag)
    prompt = ("Beantwoord de vraag van de klant met alleen "
              "deze informatie van de winkel. Staat het "
              "antwoord er niet in, zeg dat dan.\n\n"
              f"{stuk}\n\nVraag: {vraag}")
    return vraag_llm(prompt)


if __name__ == "__main__":
    for vraag in [
        "Hoeveel waarborg moet ik betalen voor een bakfiets?",
        "Quelle caution pour un vélo cargo ?",
    ]:
        print("vraag:     ", vraag)
        print("zonder RAG:", vraag_llm(vraag))
        print("gevonden:  ", zoek(vraag))
        print("met RAG:   ", antwoord_met_rag(vraag))
        print()
