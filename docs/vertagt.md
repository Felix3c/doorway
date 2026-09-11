# Doorway — Vertagte Kleinigkeiten

Befunde aus den Reviews zu Teil 3 (Zweig `hinterlegen`, gemerged 11.09.2026 als PR #1),
bewusst nicht gefixt. Keiner ändert heute die Ausgabe. Wer einen angeht: kleiner
Folge-PR, Test zuerst, wo es einen gibt. Erledigtes hier streichen.

## Seite (`site/hinterlegen-seite.js`, `site/hinterlegen.html`)

- `fehlerZeigen` sucht den Fehlerknoten fürs Feld `typ` über den Nachbarn und träfe
  einen falschen Knoten, wenn `typ` je einen Fehler bekäme. Heute unerreichbar, `typ`
  kommt aus festen Knöpfen.
- Fehlertexte stehen als `<p>` im `<label>` statt über `aria-describedby` am Feld.
  Screenreader lesen sie mit dem Label vor; die Verknüpfung wäre sauberer.
- Ein Entwurf, in dem nur der Typ „Zahl" gewählt und sonst nichts eingetragen ist, wird
  nicht gespeichert (die Leer-Prüfung zählt `typ` nicht).
- `statusNachsehen` bricht beim ersten fehlgeschlagenen Fetch ab, statt die weiteren
  Kandidaten (andere Bücher) zu probieren.
- Der Präfix-Abgleich zwischen id und Buch-Ordner stolpert bei Ordnernamen mit
  Bindestrich; degradiert sauber zu „Noch nicht aufgenommen".
- „Prüfen Sie Stichtag und Ort des Nachweises." (Spec §2, Wortlaut) steht in einer Seite,
  die sonst duzt.

## Tests (`tests/test_hinterlegen_rundlauf.py`, `site/hinterlegen.pruefung.mjs`)

- `pytest.importorskip("wettbuch")` überspringt den Rundlauf still, wenn der Generator
  nicht installiert ist. Kein pytest-CI im Repo würde das bemerken. `python -m pytest -q`
  meldet dann 128 statt 130.
- `subprocess.run(..., check=True)` liefert bei einem Node-Fehler einen Traceback statt
  einer Assertion mit Ausgabe.
- Die Fixture `BUECHER` nutzt `zweig: main`; live steht in `buecher.json` `master`.
- Es fehlen Tests für `bedingungFrist` ohne `bedingung` und für einen ungültigen `typ`.

## Ungemessen

- Ob GitHub bei einer URL nahe `PR_URL_MAX` (6400) noch vollständig vorbefüllt. Der
  Probelauf lag bei 2213 Zeichen. Prüfung: Zitat 400 und Bedingung 200 Zeichen mit vielen
  Umlauten füllen (URL dann etwa 5800), eingeloggt Knopf 1 drücken.

## Bewusst abgelehnt, nicht offen

- Deutsches Komma in Zahlen (`0,10`). Entscheidung 11.09.2026, Spec Teil 3 §10.
