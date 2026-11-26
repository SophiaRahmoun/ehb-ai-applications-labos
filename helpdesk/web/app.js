// De pagina van de helpdesk-app: de inbox, en bij een ticket wat je API erover zegt.
// Je hoeft hier niets te wijzigen: de opdrachten zitten in toon.py, lezen.py en antwoord.py.

const TEAMS = {
  facturatie: "Boekhouding",
  levering: "Logistiek",
  defect: "Werkplaats",
  account: "Klantendienst",
  verhuur: "Verhuur",
};

const lijst = document.querySelector("#tickets");
const detail = document.querySelector("#detail");
let tickets = [];
let gekozen = null;

// Maakt een HTML-element met tekst erin.
function element(tag, tekst, klasse) {
  const el = document.createElement(tag);
  if (tekst !== undefined && tekst !== null) el.textContent = tekst;
  if (klasse) el.className = klasse;
  return el;
}

async function laadInbox() {
  const antwoord = await fetch("/tickets");
  tickets = await antwoord.json();
  toonLijst();
}

async function kies(ticket) {
  gekozen = ticket;
  toonLijst();
  if (!ticket.analyse) {
    toonDetail(ticket, "Je API leest het ticket…");
    const antwoord = await fetch(`/analyse?tekst=${encodeURIComponent(ticket.tekst)}`);
    if (!antwoord.ok) {
      toonDetail(ticket, "Fout: kijk in de terminal van je API.");
      return;
    }
    ticket.analyse = await antwoord.json();
    toonLijst();
  }
  if (gekozen === ticket) toonDetail(ticket);
}

function toonLijst() {
  lijst.replaceChildren();
  for (const ticket of tickets) {
    const li = element("li", null, ticket === gekozen ? "gekozen" : "");
    li.append(element("strong", ticket.afzender), " ", element("small", ticket.tekst));
    if (ticket.status) li.append(element("small", ticket.status));
    li.addEventListener("click", () => kies(ticket));
    lijst.append(li);
  }
}

// Een tabel met wat toon.py en lezen.py over het ticket zeggen.
function kenmerken(data) {
  const v = data.kenmerken;
  const t = data.toon;
  const rij = [
    ["Team", v ? TEAMS[v.categorie] ?? v.categorie : undefined],
    ["Taal", v?.taal],
    ["Toon", t?.toon],
    ["Klant", v?.klantnummer],
    ["Factuur", v?.factuurnummer],
  ];
  const tabel = element("table");
  const kop = tabel.createTHead().insertRow();
  const waarden = tabel.createTBody().insertRow();
  for (const [naam, waarde] of rij) {
    kop.append(element("th", naam));
    const cel = waarden.insertCell();
    if (waarde === undefined) {
      cel.append(element("span", "nog niet gemaakt", "nog-niet"));
    } else {
      cel.textContent = waarde ?? "—";
    }
  }
  if (t?.toon === "negatief") waarden.cells[2].className = "negatief";
  if (t) waarden.cells[2].title = `door: ${t.door}, confidence ${t.confidence}`;
  return tabel;
}

// Het antwoord: het voorstel van antwoord.py, de bron, en de knoppen.
function antwoord(ticket) {
  const voorstel = ticket.analyse.voorstel;
  const team = TEAMS[ticket.analyse.kenmerken?.categorie] ?? "een collega";
  const blok = element("article");
  blok.append(element("header", `Antwoord aan ${ticket.afzender}`));
  const tekstvak = element("textarea");
  tekstvak.rows = 4;
  if (ticket.antwoord) {
    blok.append(element("p", "Dit antwoord is verstuurd."));
    tekstvak.value = ticket.antwoord;
  } else if (!voorstel) {
    blok.append(element("p", "Nog geen voorstel: antwoord.py is nog niet gemaakt.", "nog-niet"));
  } else if (voorstel.antwoord === null) {
    blok.append(element("p", "Geen antwoord gevonden in de kennisbank. Schrijf zelf een antwoord, of stuur het ticket door."));
  } else {
    blok.append(element("p", "Voorstel van AI. Lees het na en pas het aan voor je het verstuurt."));
    tekstvak.value = voorstel.antwoord;
  }
  blok.append(tekstvak);
  if (voorstel?.antwoord) {
    blok.append(element("small", "Gebaseerd op deze alinea uit de kennisbank:"));
    blok.append(element("blockquote", voorstel.bron));
  }
  const verstuur = element("button", "Versturen");
  verstuur.onclick = () => handelAf(ticket, "beantwoord", tekstvak.value);
  const door = element("button", `Doorsturen naar ${team}`, "secondary");
  door.onclick = () => handelAf(ticket, `naar ${team}`, null);
  blok.append(verstuur, " ", door);
  if (ticket.status) blok.append(element("p", `Status: ${ticket.status}`));
  return blok;
}

// Bewaart in de databank wat de medewerker deed, met het voorstel van de AI erbij.
async function handelAf(ticket, status, antwoord) {
  const voorstel = ticket.analyse.voorstel?.antwoord ?? null;
  // Jouw beurt: stuur status, antwoord en voorstel als JSON naar
  // POST /tickets/{id}, met het id van dit ticket. Kijk hoe nieuw.html
  // een ticket naar POST /tickets stuurt.
  const resultaat = { ok: false, status: "nog niet gemaakt" };
  if (!resultaat.ok) {
    detail.append(element("p", `Niet bewaard (${resultaat.status})`, "negatief"));
    return;
  }
  ticket.status = status;
  ticket.antwoord = antwoord;
  toonLijst();
  toonDetail(ticket);
}

function toonDetail(ticket, melding) {
  detail.replaceChildren(element("h2", ticket.afzender));
  if (melding) {
    detail.append(element("p", melding), element("blockquote", ticket.tekst));
    return;
  }
  detail.append(kenmerken(ticket.analyse), element("blockquote", ticket.tekst), antwoord(ticket));
}

laadInbox();
