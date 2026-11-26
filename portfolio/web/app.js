// Toont de voorbeelden uit voorbeelden.csv, stuurt een tekst naar /analyse, toont het
// antwoord van elke stap als een tabel, en bewaart het in de databank als je dat wilt.
// Werkt voor elke dictionary die je stappen teruggeven. Pas het gerust aan voor je eigen app.

const keuze = document.querySelector("#voorbeelden");
const tekst = document.querySelector("#tekst");
const stappen = document.querySelector("#stappen");
const bewaard = document.querySelector("#bewaard");

// Maakt een HTML-element met tekst erin.
function element(tag, inhoud, klasse) {
  const el = document.createElement(tag);
  if (inhoud !== undefined && inhoud !== null) el.textContent = inhoud;
  if (klasse) el.className = klasse;
  return el;
}

async function laadVoorbeelden() {
  const antwoord = await fetch("/voorbeelden");
  for (const voorbeeld of await antwoord.json()) {
    keuze.append(element("option", voorbeeld.tekst));
  }
}

keuze.addEventListener("change", () => {
  if (keuze.value) tekst.value = keuze.value;
});

// Eén stap: een tabel met de sleutels en waarden uit de dictionary.
function stap(naam, data) {
  const blok = element("article");
  blok.append(element("header", naam));
  if (data === null) {
    blok.append(element("p", "nog niet gemaakt", "nog-niet"));
    return blok;
  }
  const tabel = element("table");
  for (const [sleutel, waarde] of Object.entries(data)) {
    const rij = tabel.insertRow();
    rij.insertCell().append(element("strong", sleutel));
    rij.insertCell().textContent = JSON.stringify(waarde);
  }
  blok.append(tabel);
  return blok;
}

document.querySelector("#formulier").addEventListener("submit", async (event) => {
  event.preventDefault();
  stappen.replaceChildren(element("p", "Je API leest de tekst…"));
  const start = performance.now();
  const antwoord = await fetch(`/analyse?tekst=${encodeURIComponent(tekst.value)}`);
  if (!antwoord.ok) {
    stappen.replaceChildren(element("p", "Fout: kijk in de terminal van je API."));
    return;
  }
  const data = await antwoord.json();
  stappen.replaceChildren();
  for (const naam in data) {
    stappen.append(stap(naam, data[naam]));
  }
  stappen.append(element("small", `${Math.round(performance.now() - start)} ms `));
  const knop = element("button", "Bewaar", "secondary");
  knop.onclick = () => bewaar(tekst.value, data);
  stappen.append(knop);
});

// Bewaart de tekst en het resultaat in de databank.
async function bewaar(inhoud, resultaat) {
  await fetch("/resultaten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tekst: inhoud, resultaat }),
  });
  laadBewaard();
}

// Toont wat er in de databank staat: per tekst de tabellen van de stappen.
async function laadBewaard() {
  const antwoord = await fetch("/resultaten");
  bewaard.replaceChildren();
  for (const rij of await antwoord.json()) {
    const blok = element("details");
    blok.append(element("summary", `${rij.tijd} · ${rij.tekst}`));
    for (const naam in rij.resultaat) {
      blok.append(stap(naam, rij.resultaat[naam]));
    }
    bewaard.append(blok);
  }
}

laadVoorbeelden();
laadBewaard();
