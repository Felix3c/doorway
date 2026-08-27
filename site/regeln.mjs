// Regelauswertung fuer die Seite. Rechnet nichts nach: kompiliert die aus
// regeln.py exportierten Muster und wendet sie an. Wird von app.js (Browser)
// und pruefung.mjs (Node) gleichermassen benutzt.

export function kompilieren(regeln) {
  return regeln.map((r) => ({
    ...r,
    regex: r.muster !== undefined ? new RegExp(r.muster, r.flags || "") : null,
  }));
}

export function pruefen(regeln, vorhabentext, typ, mehrfachantrag) {
  return regeln.filter((r) => {
    if (r.regex) return Boolean(vorhabentext) && r.regex.test(vorhabentext);
    if (r.bedingung === "typ_firma") return typ === "Firma";
    if (r.bedingung === "mehrfachantrag") return Boolean(mehrfachantrag);
    return false;
  });
}

// Selbstpruefung: jedes exportierte Beispiel muss im Browser dasselbe
// Ergebnis liefern wie in Python. Gibt die Liste der Abweichungen zurueck.
export function selbstpruefung(regeln, beispiele) {
  const abweichungen = [];
  for (const [name, faelle] of Object.entries(beispiele)) {
    for (const [text, erwartet] of faelle) {
      const trifft = pruefen(regeln, text, null, false).some((r) => r.name === name);
      if (trifft !== erwartet) abweichungen.push({ name, text, erwartet, trifft });
    }
  }
  return abweichungen;
}
