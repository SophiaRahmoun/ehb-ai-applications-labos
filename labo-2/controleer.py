from hulp import evalueer
from lokaal_taalmodel import lees_met_lokaal_taalmodel

NUMMERS = ["klantnummer", "factuurnummer", "bestelnummer"]


def controleer(antwoord, tekst):
    for veld in NUMMERS:
        nummer = antwoord.get(veld)

        if nummer is not None and nummer not in tekst:
            antwoord[veld] = None

    return antwoord



#def lees_met_controle(tekst):
    # Opdracht: vraag het aan het lokale taalmodel,
    # en controleer dan het antwoord.
   # return lees_met_lokaal_taalmodel(tekst)

def lees_met_controle(tekst):
    antwoord = lees_met_lokaal_taalmodel(tekst)
    return controleer(antwoord, tekst)

def lees_met_opnieuw_vragen(tekst):
    antwoord = lees_met_lokaal_taalmodel(tekst)

    fouten = []

    for veld in NUMMERS:
        nummer = antwoord.get(veld)

        if nummer is not None and nummer not in tekst:
            fouten.append(
                f"Let op: {nummer} staat niet in dit ticket."
            )

    if fouten:
        nieuwe_tekst = tekst + "\n\n" + "\n".join(fouten)
        antwoord = lees_met_lokaal_taalmodel(nieuwe_tekst)

    return controleer(antwoord, tekst)


if __name__ == "__main__":
    evalueer(lees_met_controle)
    # evalueer(lees_met_opnieuw_vragen)


