from .hulp import evalueer


def voorspel_met_regel(tekst):
    if "kapot" in tekst or "inadmissible" in tekst or "alweer" in tekst or "niet" in tekst or "geen" in tekst:
        return "negatief"
    return "positief"


evalueer(voorspel_met_regel)
