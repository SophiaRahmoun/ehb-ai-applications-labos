import re

from hulp import evalueer_zoeken, stukken

DREMPEL = 1


def woorden(tekst):
    return set(re.findall(r"\w{4,}", tekst.lower()))


def overlap(vraag, stuk):
    return len(woorden(vraag) & woorden(stuk))


def zoek_op_woorden(vraag):
    beste = stukken[0]
    for stuk in stukken:
        if overlap(vraag, stuk) > overlap(vraag, beste):
            beste = stuk
    score = overlap(vraag, beste)
    if score < DREMPEL:
        return {"stuk": None, "score": score}
    return {"stuk": beste, "score": score}


evalueer_zoeken(zoek_op_woorden)
