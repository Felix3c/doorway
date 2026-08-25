# Datenlage-Recherche: Wo lässt sich das Nein-Register füllen?

**Datum:** 2026-08-24
**Auftrag:** Punkt 1 aus `NAECHSTE-SCHRITTE.md` — systematischer Durchgang durch die Landtags-Dokumentensuche, Ergebnis: Rangliste von 2–3 Programmfamilien nach Datenverfügbarkeit, daraus folgt der Brückenkopf.
**Status:** abgeschlossen. Ein Durchlauf, Ergebnis unten. Es wurde nichts gebaut.
**Zugehörige Spec:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (§5.4 Register, §7 Kaltstart, §11 offene Punkte)

---

## 0. Das Ergebnis in vier Sätzen

Der Brückenkopf ist die **Heimatförderung des Landes NRW** — heute „Starke Heimat Nordrhein-Westfalen", 2018–2022 „Heimat. Zukunft. Nordrhein-Westfalen." — mit ihren fünf Förderelementen Scheck, Preis, Fonds, Werkstatt, Zeugnis.

Sie ist die einzige geprüfte Programmfamilie, für die **Antragszahlen, Bewilligungen, Ablehnungen und Ablehnungsgründe** über mehrere Jahre öffentlich, kostenlos und in maschinenlesbarer Form vorliegen — und für die diese Zahlen **jedes Frühjahr neu erscheinen**, ohne dass jemand eine Anfrage stellen muss.

Der entscheidende methodische Fund: Die Ader liegt **nicht** in den Drucksachen (Kleine Anfragen und ihre Antworten), sondern in den **Vorlagen** — den jährlichen Berichten des Ministeriums an den Ausschuss für Heimat und Kommunales. Die Landtags-Suche „Anfragen und Antworten" findet diese Klasse gar nicht; dafür braucht es die Parlamentsdatenbank.

Von 140 im Volltext geprüften Antwort-Drucksachen aus dem gesamten Förder-Umfeld enthalten **101 das Wort „abgelehnt" kein einziges Mal**. Ablehnungsdaten sind in NRW nicht knapp — sie sind fast nicht existent. Genau das macht sie zum Rohstoff.

---

## 1. Methode

### 1.1 Was durchsucht wurde

| Quelle | Zugang | Umfang |
|---|---|---|
| Landtag NRW, Dokumentensuche „Anfragen und Antworten" | `anfragen-und-antworten-suchergeb.html?suchwort=…&wp=…&page=…` (GET, zustandslos) | 62 Abfragen, WP 10–18 (seit 1985) |
| Landtag NRW, **Parlamentsdatenbank** (inkl. Vorlagen `MMV…`, Ausschussprotokolle) | `parlamentsdatenbank-suchergebnis.html?suchwort=…` (GET, zustandslos) | 21 gezielte Abfragen |
| Drucksachen-/Vorlagen-PDFs | `…/dokumentenarchiv/Dokument/MMD<WP>-<Nr>.pdf` bzw. `MMV<WP>-<Nr>.pdf` | 159 PDFs, 347 MB |
| fragdenstaat.de | REST-API `v1` + HTML-Suche | Schema geprüft, Stichproben |
| efre.nrw Liste der Vorhaben | CSV, 5,2 MB | vollständig geladen und geprüft |
| NRW.BANK | Web/Presse | geprüft |

**Ertrag über alle Abfragen:** 8.674 deduplizierte Dokumentnachweise, davon 2.187 Anfragen und 1.541 Antworten (der Rest sind Vorlagen, Anträge, Gesetzentwürfe und Protokolle, die die Suche mitliefert).

### 1.2 Drei Phasen

1. **Kataster** — breite Trefferlisten über Thesaurus-Schlagworte (`Förderung`, `Landesmittel`, `Wirtschaftsförderung` …) und über 26 Programmnamen. Nur Metadaten, keine PDFs.
2. **Zielsuche** — 19 Phrasen, die *im Abstract* stehen, wenn eine Anfrage nach Ablehnungen fragt: „abgelehnte Förderanträge", „Ablehnungsgründe", „bewilligte und abgelehnte", „Bewilligungsquote" …
3. **Belegprobe** — 140 Kandidaten-Antworten wirklich heruntergeladen, in Text gewandelt und im Volltext gezählt: Vorkommen von „abgelehnt", Existenz eines Ablehnungsgrunds, Anzahl Tabellenzeilen mit Status **und** Betrag.

### 1.3 Zwei Dinge, die man wissen muss, bevor man das nachbaut

**Die Suche greift auf den Dokumentnachweis, nicht auf den PDF-Volltext.** Indexiert sind Titel, Abstract, Schlagworte, Region und Systematik. Deshalb funktionieren Abstract-Phrasen präzise — und deshalb findet eine Suche nach „abgelehnt" *nicht*, was in einer Tabelle auf Seite 87 steht.

**Seitenzahl ist ein Vorfilter, kein Beleg.** Eine Anfrage hat 1 Seite, eine Antwort mit Datenanhang 47 bis 139. Aber Drs 17/13951 „Moderne Sportstätte 2022" hat 142 Seiten und enthält *drei* Vorkommen von „abgelehnt" — es ist eine Mittelabruf-Tabelle. Jeder Kandidat wurde deshalb im Volltext gegengeprüft.

### 1.4 Nachvollziehbarkeit

Werkzeuge und Rohdaten liegen unter `research/`: `ltsearch.py` (Suche), `harvest_a.py` / `harvest_b.py` (Kataster, Zielsuche), `score_pdfs.py` (Belegprobe), `extract_tables.py` und `zeilen.py` (Tabellen), `raw/*.json` (63 Trefferlisten), `belegprobe.json` (140 Volltextbefunde), `pdf/` (Quelldokumente). Jede Zahl in diesem Bericht ist auf ein benanntes Dokument mit Datum zurückführbar.

---

## 2. Die Quellenlandschaft — vier Klassen, sehr ungleich

### Klasse A — Vorlagen: jährliche Ministeriumsberichte an die Fachausschüsse

**Das ist die Ader.** Ministerien berichten den Ausschüssen jährlich über ein Förderprogramm. Diese Berichte tragen die Tabellen. Sie sind öffentlich, kostenlos und erscheinen im festen Rhythmus.

Warum das bisher übersehen wurde: Die Landtags-Suche „Anfragen und Antworten" indexiert diese Klasse **nicht**. Der Weg dorthin führte über die Antworten von 2025, die nicht mehr antworten, sondern *weiterverweisen* — Drs 18/14166 verweist auf `Vorlage 18/3926`.

### Klasse B — Antwort-Drucksachen auf Kleine/Große Anfragen

Der wertvollste Einzelfund liegt hier: **Drs 17/9738** (12.06.2020, 139 S.), Antwort auf eine SPD-Anfrage, mit einer Anlage über **3.317 Einzelanträge** der Heimatförderung 2018–2019, jeder mit Status und Ablehnungsgrund. Dieselbe Anlage wurde vielfach an wahlkreisbezogene Antworten gehängt — eine Massenanfrage der SPD-Fraktion vom 12.06.2020.

Aber: Die Belegprobe über 140 Antworten zeigt, dass das die Ausnahme ist.

| Vorkommen von „abgelehnt" | Anzahl Antworten |
|---|---|
| 0 | 101 |
| 1–4 | 35 |
| 5–19 | 3 |
| 20+ | 1 |

Antworten mit ≥ 20 Tabellenzeilen, die Status **und** Betrag tragen: **3 von 140.**

### Klasse C — Pflichtveröffentlichungen (EU-kofinanziert)

**Geprüft und für das Nein-Register untauglich.** Die EFRE/JTF-Liste der Vorhaben (CSV, 3.637 Zeilen) hat 17 Spalten: `Programm, Priorität, Spezifisches Ziel, ID, Bezeichnung, Beginn, Ende, Standort, Art der Intervention, Gesamtkosten, Fonds, Kofinanzierungssatz, Name des Begünstigten` — **keine Statusspalte, keine Ablehnungen**, dafür Klarnamen der Bewilligten. Sie zeigt strukturell genau die, die durchgekommen sind. Dasselbe gilt für die Europa-Scheck-„Zusagenliste" (1.607 Zeilen, Stichtage 1–5, 2024) und die Umweltscheck-Listen des MUNV.

Das ist keine Lücke, sondern eine Bauart: EU-Recht verlangt die Veröffentlichung der *Begünstigten*. Niemand ist verpflichtet, die Abgewiesenen zu zählen.

### Klasse D — fragdenstaat.de

Die REST-API (`/api/v1/request/`) hat **keine Volltextsuche** — Filter sind `jurisdiction`, `public_body`, `status`, `resolution`, `campaign`, `tags`, `costs_min/max`, `created_at_*`. NRW ist `jurisdiction=nrw` (ID 2). Für gezielte Recherche muss man die HTML-Suche `fragdenstaat.de/anfragen/?q=…&jurisdiction=nrw` scrapen; die Relevanz ist mäßig. Als *Ergänzung* brauchbar, als Fundament nicht.

---

## 3. Rangliste der Programmfamilien nach Datenverfügbarkeit

Bewertet nach den Kriterien aus `NAECHSTE-SCHRITTE.md`: Antragszahlen? Bewilligungszahlen? Ablehnungszahlen? Ablehnungsgründe? Über wie viele Jahre? Wie oft wird nachgefragt?

| # | Programmfamilie | Anträge | Bewilligt | Abgelehnt | Gründe | Jahre | Rhythmus | Urteil |
|---|---|---|---|---|---|---|---|---|
| **1** | **Heimatförderung / Starke Heimat NRW** | ja | ja | ja | ja, je Antrag | 2018, 2019, 2021, 2023, 2024, 2025 | jährlich, Frühjahr | **Brückenkopf** |
| 2 | DFG-Sonderforschungsbereiche (NRW-Anteil) | teilw. | ja | ja, namentlich | nein | laufend | halbjährlich | Nebenader |
| 3 | Umwelt-Scheck / Europa-Scheck | teilw. | ja | nein | nein | 2023– | jährlich | nur Positivlisten |
| 4 | Wohnraumförderung | teilw. | ja | nein | nein | 31 | häufig | keine Ablehnungsdaten |
| 5 | EFRE / EU-Mittel | teilw. | ja | nein | nein | 32 | laufend | Begünstigtenliste, Mittelabfluss |
| 6 | Städtebau, Kultur, Denkmal, Sport, Kita, Breitband, Digitalpakt | teilw. | teilw. | nein | nein | viele | viele | Volumen statt Verfahren |
| 7 | Gründungsstipendium NRW | nein | teilw. | nein | nein | — | — | **hohe Erzählkraft, keine Daten** |

### Platz 1 — Heimatförderung: die Belege

**Drs 17/9738** (12.06.2020, 139 S.) — Anlage mit 3.317 Einzelanträgen 2018–2019. Spalten: `Lfd. Nr. | Regierungsbezirk | Kommune | Förderelement | Antragstellertyp | Fördergegenstand | Fördersumme | Antragsdatum | Entscheidungsdatum | Status | Ablehnungsgrund`. Maschinell sauber extrahierbar (PyMuPDF, 11 Spalten).

Daraus errechnete Basisraten:

| Antragsjahr | gesamt | bewilligt | abgelehnt | Ablehnungsquote |
|---|---|---|---|---|
| 2018 | 1.420 | 912 | 508 | **35,8 %** |
| 2019 | 1.893 | 1.185 | 708 | **37,4 %** |

Und nach Förderelement (2018+2019):

| Element | gesamt | bewilligt | abgelehnt | Ablehnungsquote |
|---|---|---|---|---|
| Heimat-Scheck | 2.942 | 1.811 | 1.131 | 38,4 % |
| Heimat-Preis | 178 | 177 | 1 | 0,6 % |
| Heimat-Fonds | 66 | 50 | 16 | 24,2 % |
| Heimat-Werkstatt | 40 | 19 | 21 | **52,5 %** |
| Heimat-Zeugnis | 90 | 41 | 49 | **54,4 %** |

Häufigste Ablehnungsgründe (2018–2019, 1.219 Fälle): „entspricht nicht den Förderkriterien" (556), „Vereinsausstattung" (130), „vereinsintern" (122), „vereinsübliche Ausstattung" (27), „vorzeitiger Maßnahmenbeginn" (18), „Antrag nicht prüffähig" (13).

**Vorlage 17/6633** (22.03.2022, 56 S.) — „Übersicht Heimatförderung 2021", exakt im Schema, das §5.4 der Spec verlangt:

| Element | Anträge | bewilligt | abgelehnt | Fördervolumen |
|---|---|---|---|---|
| Scheck | 1.125 | 850 | 275 | 1.700.000,00 € |
| Preis | 243 | 243 | 0 | 1.395.000,00 € |
| Fonds | 33 | 31 | 2 | 539.096,27 € |
| Werkstatt | 46 | 40 | 6 | 2.727.081,65 € |
| Zeugnis | 66 | 55 | 11 | 18.779.831,95 € |
| **Gesamt** | **1.513** | **1.219** | **294** | **25.141.009,87 €** |

**Vorlage 18/3926** (23.05.2025, 47 S.) — Förderjahr 2024, je Bewilligungsbehörde:

| Bezirksregierung | bewilligt | Bewilligung € | abgelehnt | Ablehnungsquote |
|---|---|---|---|---|
| Arnsberg | 261 | 1.250.068 | 147 | 36,0 % |
| Detmold | 202 | 1.729.802 | 92 | 31,3 % |
| Düsseldorf | 162 | 1.705.400 | 65 | 28,6 % |
| Köln | 134 | 551.769 | 87 | **39,4 %** |
| Münster | 124 | 2.068.269 | 36 | **22,5 %** |
| **Gesamt** | **883** | **7.305.308** | **427** | **32,6 %** |

**Vorlage 18/5027** (21.04.2026, 39 S.) — Förderjahr 2025, aktuellster Stand: 947 Bewilligungen, 7.530.611 €; Heimat-Scheck 598 bewilligt (2024: 550), 329 Ablehnungen (2024: 396). Anlage mit Einzelanträgen, Spalten `Kommune | Förderbereich | Kurzbezeichnung des Vorhabens | Fördernehmende | Bewilligung (in Euro) | Ablehnung | Ablehnungsgrund`.

**Vorlage 18/2806** (19.07.2024, 112 S.) — Förderjahr 2023, „Anlage 3: Abgelehnte Anträge an das Landes-Förderprogramm ‚Starke Heimat Nordrhein-Westfalen'", Spalten `Durchführungsort | Förderelement | Vorhaben/Projektbezeichnung | Ablehnungsgrund`. Rund 538 Zeilen mit Grund.

**Vorlage 17/2268** (05.07.2019, 94 S.) — „Übersicht der abgelehnten Anträge der Heimatförderung für 2018", rund 391 Zeilen mit Grund.

**Abdeckung und Lücken:**

| Förderjahr | Ablehnungszahlen | Ablehnungsgründe | Quelle |
|---|---|---|---|
| 2018 | ja, 508 | ja, je Antrag | Drs 17/9738, Vorl 17/2268 |
| 2019 | ja, 708 | ja, je Antrag | Drs 17/9738 |
| 2020 | nein | nein | Vorl 17/5310 (8 S.) enthält keine — **Lücke** |
| 2021 | ja, 294 | nur aggregiert | Vorl 17/6633 |
| 2022 | nein | nein | Vorl 18/863 (87 S.) enthält keine — **Lücke** |
| 2023 | ja | ja, je Antrag | Vorl 18/2806 |
| 2024 | ja, 427, je BezReg | nur Prosa | Vorl 18/3926 |
| 2025 | ja, 329 (Scheck) | ja, je Antrag | Vorl 18/5027 |

Sechs von acht Förderjahren belegt, davon vier mit Gründen auf Antragsebene. Die zwei Lücken (2020, 2022) sind genau die Fälle für gezielte IFG-Anfragen nach §7 der Spec — zwei Anfragen statt eines Feldzugs.

### Platz 2 — DFG-Sonderforschungsbereiche

Vorl 18/3954 (05.06.2025) und Vorl 18/4641 (03.12.2025) tragen je eine Anlage „Sitzung DFG-Bewilligungsausschuss für die SFB … — **Abgelehnte NRW-Anträge** (Sprecher- und Beteiligungsfunktion)". Halbjährlicher Rhythmus, Ablehnungen namentlich (Institutionen, keine natürlichen Personen). Aber: keine Ablehnungsgründe, kleine Fallzahlen, und die Zielgruppe sind Universitäten — nicht die Ausgesperrten der These. Als Nebenader interessant, als Brückenkopf verfehlt.

### Platz 7 — Gründungsstipendium NRW: der Fall, der die Regel bestätigt

Das Programm liegt Doorway am nächsten — und ist als Datenquelle das schwächste Ergebnis der Recherche. Antrags- und Ablehnungszahlen werden nicht veröffentlicht; die jüngste Antwort (Drs 18/20056, 19.06.2026) beantwortet Haushaltsfragen und schweigt zu Antragszahlen.

Erzählerisch ist es dafür der stärkste Fund des Laufs. Wörtlich aus derselben Antwort:

> „Zur Reduzierung der Antragszahlen aufgrund der geringeren Haushaltsmittel wurden die Vorgaben zur Bewertung der Geschäftsmodelle durch die Jury **zweimal verschärft**."

Und: Seit Frühjahr 2026 sind die Jurysitzungen ausgesetzt. Die Schwelle wurde nicht erhöht, weil die Anträge schlechter wurden, sondern weil das Geld knapper wurde — mit dem erklärten Ziel, die Zahl der Versuche zu senken. Das ist §2 der Spec in der Sprache des Ministeriums.

Genau deshalb steht dieses Programm auf Platz 7 und nicht auf Platz 1. Die Spec sagt: *„Brückenkopf-Entscheidung: bewusst nach Datenlage statt nach Zielgruppen-Sympathie. Ein Register, das sich nicht füllen lässt, ist kein Projekt."* Hier ist der Fall, an dem diese Regel greift.

---

## 4. Empfehlung: der Brückenkopf

**Heimatförderung NRW (Starke Heimat), Förderjahre 2018–2025, Register-Granularität: Programm × Förderelement × Jahr × Bezirksregierung.**

Fünf Gründe, in der Reihenfolge ihres Gewichts:

1. **Die Daten existieren, mit Gründen, über sechs Jahre.** Kein anderes geprüftes Programm kommt in die Nähe.
2. **Sie erneuern sich von selbst.** Der Ausschussbericht kommt jedes Frühjahr. Der Bericht für 2025 ist vier Monate alt. Das Register veraltet nicht, solange der Ausschuss tagt — ohne eine einzige IFG-Anfrage.
3. **Die Zielgruppe ist exakt die der These.** Vereine, Initiativen, Privatpersonen. Antragssummen ab 2.000 €. Menschen ohne Antragsabteilung, ohne Berater, ohne Vorfinanzierung. Kein Fördermittelberater arbeitet für 5 % von 2.000 €. Der Markt ist unbesetzt, weil er sich für die Gegenseite nicht rechnet — das ist die Asymmetrie aus §4 der Spec.
4. **Die Ablehnungsgründe sind prognostizierbar und vermeidbar.** „Vereinsausstattung", „vereinsintern", „vorzeitiger Maßnahmenbeginn", „mehrere Anträge desselben Antragstellers im Jahr" — das sind keine Qualitätsurteile, das sind Regelverstöße, die niemand vorher gesagt hat. Der Spiegel und die Prognose aus §5 können hier realen Schaden verhindern.
5. **Die Ungleichbehandlung ist amtlich belegt.** Das Ministerium schreibt in Vorl 18/3926 selbst:

   > „…zeigt sich immer noch eine **uneinheitliche Bewilligungspraxis in den Bezirksregierungen** im Hinblick auf die Behandlung von Antragstellungen."

   Die Zahlen dazu: Münster lehnt 22,5 % ab, Köln 39,4 %. Gleiches Programm, gleiche Richtlinie, 1,75-facher Unterschied — je nachdem, wo jemand wohnt. Das ist die Schwelle aus §2, gemessen und von der Bewilligungsbehörde eingeräumt.

**Was das für §10 der Spec bedeutet.** Der Leitplanken-Test lautet: fliegt raus, was nur Sinn ergibt, um die Gegenseite bloßzustellen. Punkt 5 besteht diesen Test, weil er *nützlich* ist: Wer in Köln einen Heimat-Scheck beantragt, sollte wissen, dass seine Chance schlechter steht als in Münster. Das ist keine Anklage, das ist eine Prognose. Die Bloßstellung wäre, daraus eine Behördenrangliste zu machen — das verbietet §6 ohnehin.

---

## 5. Negative Befunde — was ausdrücklich nicht funktioniert

Diese Punkte sind so wichtig wie die positiven, weil sie Monate sparen.

- **EFRE-Empfängerlisten füllen das Register nicht.** Keine Statusspalte, nur Bewilligte. §7 Punkt 3 der Spec muss heruntergestuft werden: von „Beschaffungsquelle" zu „Kontext- und Nennerquelle".
- **NRW.BANK veröffentlicht Volumina und Beratungszahlen, keine Ablehnungsquoten.** Für das Register unbrauchbar.
- **Die Antworten auf Kleine Anfragen sind 2025 dünn geworden.** Die 53 Antworten der Scheck-Serie vom 04.06.2025 sind je 2 Seiten und verweisen weiter. Wer nur Drucksachen erntet, findet ab 2024 fast nichts mehr.
- **Umwelt-Scheck: die Ablehnungen sind gelöscht.** Wörtlich aus Vorl 18/3566 (07.02.2025, MUNV):

  > „Die Nachverfolgung der abgelehnten Anträge ist aufgrund eines **Programmfehlers des neuen Online-Verfahrens** nicht mehr rückwirkend möglich. Da die Fehlerquelle nun bekannt ist, wird das Verfahren zur Bearbeitung der Anträge in diesem Jahr dementsprechend angepasst, wodurch auch die abgelehnten Anträge nun im System hinterlegt bleiben."

  Für den Umwelt-Scheck 2024 sind die Abgelehnten nicht schwer zu bekommen — sie existieren nicht mehr. Das ist die These in ihrer buchstäblichsten Form: die Ausgesperrten sind unsichtbar, weil das System sie nicht aufgehoben hat. Und es ist eine harte Grenze für das Register: dieses Programmjahr ist nicht rekonstruierbar, von niemandem.

---

## 6. Ein Fund über den Auftrag hinaus: die Landkarte

Die FDP-Fraktion hat mit zwei Großen Anfragen die gesamte Förderlandschaft abfragen lassen:

- **Drs 18/10430** (27.08.2024, 57 S.) — „Bürokratische Mittelverschwendung im immer intransparenteren Förderdschungel". Stichtag 01.05.2024: **223 landeseigene Förderprogramme**, dazu 11 der EU und 32 des Bundes mit Landesbeteiligung.
- **Drs 18/14720** (08.07.2025, 119 S.) — „Förderdschungel Nordrhein-Westfalen — Bestandsaufnahme und Entwicklung der gesamten Förderlandschaft". Rund 1.021 Fördermaßnahmen im Bestand (weiter gefasster Begriff). Die Tabelle führt je Maßnahme u. a. `Ressort, Ziel, Art, Haushaltskapitel/-titel, geplantes Gesamtausgabevolumen, bewilligende Stelle, Ist-Ausgaben 2021–2024, Plan 2025, maximale und minimale Förderung, durchschnittliche Auszahlungsdauer, Digitalisierung des Förderverfahrens, Evaluation`.

Zwei Dinge folgen daraus.

**Erstens, für den Bau:** Das ist die Programm-Dimension des Registers, fertig enumeriert. Wer wissen will, welche Programme es überhaupt gibt, muss nicht suchen — die Liste liegt vor. (Die Spaltenköpfe brechen in der PDF-Extraktion um; eine saubere Auswertung braucht koordinatenbasiertes Parsen, kein reines `pdftotext`.)

**Zweitens, für die These:** In der Vorbemerkung zu Drs 18/10803 steht der Satz, der die Marktlücke amtlich macht:

> „Letztmalig wurde im Jahr 2007 von der Landesregierung ein sogenannter ‚Förderbericht' veröffentlicht. Seitdem werden Parlament und Öffentlichkeit nicht oder nur unzureichend über die Förderlandschaft des Landes informiert."

Seit **19 Jahren** gibt es keine Gesamtübersicht darüber, was das Land fördert. Nicht für Bürger, nicht einmal für das Parlament, das den Haushalt beschließt. Doorway baut also nicht gegen einen bestehenden Transparenzstandard an — es gibt keinen.

---

## 7. Konsequenzen für die Spec

| Stelle | Bisher | Neu |
|---|---|---|
| §7, Beschaffungsreihenfolge Punkt 1 | „Landtags-Drucksachen systematisch durchsuchen" | **„Vorlagen der Fachausschüsse zuerst, Drucksachen zweitens."** Die Drucksachen-Suche allein hätte die Ader verfehlt. |
| §7, Punkt 3 (EU-Pflichtveröffentlichungen) | Beschaffungsquelle, „noch zu prüfen" | **Geprüft: keine Ablehnungsdaten.** Herabstufen zu Kontext-/Nennerquelle. |
| §7, Punkt 2 (IFG-Anfragen) | „für die Lücken" | **Konkretisiert: zwei Anfragen** — Heimatförderung 2020 und 2022. Aggregate, abgeschlossene Jahre, damit am unteren Gebührenrand. |
| §5.4, Register aggregiert | Entwurfsentscheidung | **Durch die Quellenlage bestätigt.** Die Landesregierung schwärzt Antragstellende selbst (Drs 17/9738: „zum Schutz ihrer personenbezogenen Daten nicht mit Namen genannt"; Namensfassung nur als vertrauliche Vorlage an Abgeordnete). Die öffentliche Fassung ist bereits pseudonymisiert — Doorway muss nichts weglassen. |
| §11, „Welche Programmfamilie hat die beste Datenlage?" | blockierend, offen | **Geschlossen.** Heimatförderung. Begründung siehe §4 dieses Berichts. |

---

## 8. Was als Nächstes dran ist

Der Brückenkopf steht. Damit ist der blockierende Punkt vor Abschnitt 3 des Designs weg.

**Nächster Schritt: Abschnitt 3 der Spec** — Prognose-Mechanik, Register-Datenmodell, Teststrategie. Drei Dinge, die diese Recherche dafür vorgibt:

1. **Das Register-Datenmodell hat eine belegte Zielform.** Vorl 17/6633 zeigt sie: `Förderelement | Anträge | bewilligt | abgelehnt | Fördervolumen`, je Jahr. Vorl 18/3926 fügt die Dimension `Bewilligungsstelle` hinzu — und die ist nicht kosmetisch, sie erklärt einen Teil der Varianz.
2. **Die Prognose hat belegte Basisraten.** Ablehnungsquote Heimat-Scheck 2018–2019: 38,4 %. Heimat-Zeugnis: 54,4 %. Heimat-Preis: 0,6 %. Der Unterschied zwischen den Elementen ist größer als jeder plausible Personeneffekt — das ist der erste Prädiktor, noch vor allem, was ein Nutzer eingibt.
3. **Die Extraktion ist Arbeit, aber lösbare Arbeit.** Die Tabellen aus Drs 17/9738 lesen sich sauber mit `find_tables()`. Die Vorlagen-Tabellen haben keine Linien und brauchen koordinatenbasiertes Zeilen-Clustering. Beides ist in `research/` prototypisch vorhanden — aber bewusst **nicht** als Pipeline gebaut, weil die Reihenfolge aus `NAECHSTE-SCHRITTE.md` gilt: erst Abschnitt 3, dann Implementierungsplan, dann Code.

**Was offen bleibt und Felix entscheiden muss** (unverändert aus `NAECHSTE-SCHRITTE.md`): das Zeitbudget, und ob `messen` oder belegbar.eu in Doorway aufgehen.

---

## 9. Belegliste

| Dokument | Datum | S. | Was drin steht |
|---|---|---|---|
| [Drs 17/9738](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMD17-9738.pdf) | 12.06.2020 | 139 | 3.317 Einzelanträge Heimatförderung 2018–2019, Status + Ablehnungsgrund |
| [Vorl 17/2268](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV17-2268.pdf) | 05.07.2019 | 94 | „Übersicht der abgelehnten Anträge der Heimatförderung für 2018" |
| [Vorl 17/5310](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV17-5310.pdf) | 14.06.2021 | 8 | Heimatförderung 2020 — **ohne** Ablehnungsdaten (Lücke belegt) |
| [Vorl 17/6633](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV17-6633.pdf) | 22.03.2022 | 56 | „Übersicht Heimatförderung 2021": Anträge/bewilligt/abgelehnt je Element |
| [Vorl 18/863](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-863.pdf) | 24.02.2023 | 87 | Förderjahr 2022 — **ohne** Ablehnungsdaten (Lücke belegt) |
| [Vorl 18/2806](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-2806.pdf) | 19.07.2024 | 112 | „Anlage 3: Abgelehnte Anträge … Förderjahr 2023" mit Gründen |
| [Vorl 18/3926](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-3926.pdf) | 23.05.2025 | 47 | Förderjahr 2024: 883/427 je Bezirksregierung; „uneinheitliche Bewilligungspraxis" |
| [Vorl 18/5027](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-5027.pdf) | 21.04.2026 | 39 | Förderjahr 2025: 947 Bewilligungen, 329 Ablehnungen, Anlage mit Gründen |
| [Vorl 18/3566](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-3566.pdf) | 07.02.2025 | 5 | Umwelt-Scheck: Ablehnungen wegen Programmfehler nicht mehr nachverfolgbar |
| [Drs 18/10430](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMD18-10430.pdf) | 27.08.2024 | 57 | 223 landeseigene Förderprogramme, Stichtag 01.05.2024 |
| [Drs 18/14720](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMD18-14720.pdf) | 08.07.2025 | 119 | Gesamte Förderlandschaft, ~1.021 Maßnahmen, inkl. Auszahlungsdauer |
| [Drs 18/10803](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMD18-10803.pdf) | 24.09.2024 | 9 | „Letztmalig wurde im Jahr 2007 … ein Förderbericht veröffentlicht" |
| [Drs 18/20056](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMD18-20056.pdf) | 19.06.2026 | 2 | Gründungsstipendium: Jury-Vorgaben „zweimal verschärft", Sitzungen ausgesetzt |
| [Vorl 18/3954](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-3954.pdf) / [18/4641](https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMV18-4641.pdf) | 2025 | 4/8 | DFG-SFB: „Abgelehnte NRW-Anträge", halbjährlich |
| [EFRE Liste der Vorhaben](https://www.efre.nrw/sites/default/files/media/document/file/liste_der_vorhaben_1.csv) | laufend | CSV | 3.637 Vorhaben, 17 Spalten, keine Ablehnungen |
