# Doorway — Design Teil 3: Der Hinterlegungs-Pfad

**Stand:** 05.09.2026. Entschieden von Felix mit Claude in zwei Sitzungen (02.09. und 05.09.).
**Voraus:** Teil 1 (`2026-08-24-doorway-design.md`, Präambel = Leitsatz) und Teil 2
(`2026-08-27-doorway-teil-2-design.md`). Zielbild vom 01.09.: Doorway ist der Zugang zu
allem, was Bindung belohnt. Format: festgehalten v1 (`~/wettbuch/FORMAT.md`, Repo
https://github.com/Felix3c/festgehalten, Seite https://felix3c.github.io/festgehalten/).

Ausgangspunkt sind die sechs Befunde der Probe-Hinterlegung vom 01.09.
(`research/hinterlegung-probe/BEFUNDE.md`, privat). Die Probe bleibt Probe; Teil 3 ist
das Werkzeug.

---

## 0. Was gebaut wird, in einem Absatz

Eine Seite `hinterlegen.html` auf Doorway, auf der jemand, der etwas von anderen will,
vorab und öffentlich festhält, was er erwartet. Die Seite fragt in sieben Schritten,
übersetzt die Antworten in eine Datei im festgehalten-Format und gibt sie dem
Hinterlegenden in die Hand: als vorausgefüllter Pull Request an das Zielbuch, als
Download oder per Mail. Doorway betreibt keinen Server, speichert nichts und führt kein
Buch. Die Aufnahme geschieht im Repo festgehalten durch den Halter; der Merge-Commit ist
der Zeitpunkt der Hinterlegung.

## 1. Entscheidungen zu den sechs Befunden (02.09.2026)

| Befund | Entscheidung |
|---|---|
| 1 `quelle` | Immer gefüllt, ohne Ausnahme. Eigene öffentliche Veröffentlichung des Hinterlegenden, sonst die URL der Datei im Buch. Keine Formatänderung. |
| 2 Bedingungen | Keine Formatänderung. Eine Bedingung („wenn bewilligt") steht mit eigener Frist im Vermerk. Das Formular setzt `verfall_am` selbst auf `pruefung_am` plus sechs Monate; der Hinterlegende wählt nicht. |
| 3 Beleg | Das Formular erzwingt vorab die öffentliche URL des Ortes, an dem das Ergebnis am Stichtag sichtbar sein wird. Ein Schnappschuss dieses Ortes ohne Artefakt am Prüftag ist ein gültiger Beleg für Nein. |
| 4 Zielbuch | Buch der Institution, wenn es eins gibt; sonst das Sammelbuch „Hinterlegt". Hinterlegte Einträge stehen neben zitierten und werden gleich gezählt (FORMAT §8.4). |
| 5 Halter | Der Halter hinterlegt nicht im eigenen Buch. Kein Halter ist im Werkzeug fest verdrahtet. Felix' eigener Eintrag ist nicht Teil 3. |
| 6 Festpreis | 0 Euro. Ein Preis über null wird erst veröffentlicht, wenn als Halter des Buches eine eingetragene gemeinnützige Körperschaft steht und der Betreiber von Doorway eine davon verschiedene eingetragene Gesellschaft ist. Beides ist im Vereins- bzw. Handelsregister nachprüfbar. |

Warum Verfall nach sechs Monaten statt zwei Jahren: Bei zitierten Einträgen schützt der
Verfall den Halter, der keinen Beleg findet. Bei hinterlegten Einträgen kontrolliert der
Hinterlegende den Beleg selbst; ein später Verfall verlängert nur, wie lange stilles
Ausweichen unsichtbar bleibt. Wer ein öffentliches Artefakt versprochen hat, braucht
keine zwei Jahre, um darauf zu zeigen.

Weitere Entscheidung: Bei Ja/Nein gilt nur `wert: 1.00`, `art: angekuendigt`. Die
Hinterlegung ist eine Ankündigung gegenüber dem, der vergibt, keine Wette gegen den
Computer. Wer unsicher ist, stellt die Frage weicher.

## 2. Ablauf und Datenfluss

Fünf Stationen, drei davon außerhalb von Doorway.

1. **Seite öffnen.** `hinterlegen.html` lädt die Buchliste aus `site/daten/buecher.json`
   (Kopie, siehe §5.2). Kein Laden von fremden Origins beim Ausfüllen.
2. **Ausfüllen.** Sieben Schritte in der Reihenfolge, die eine prüfbare Frage erzwingt
   (§3). Jede Eingabe wird sofort geprüft, Fehler stehen am Feld.
3. **Datei erzeugen.** Aus den Eingaben entsteht `<id>.md` mit YAML-Kopf nach FORMAT §1
   und den Textteilen Kontext, Übersetzung, Nachweis und Begründung. Die Datei wird
   vollständig angezeigt, mit dem Satz darüber: „Das hier wird nach Aufnahme nicht mehr
   geändert. Prüfen Sie Stichtag und Ort des Nachweises."
4. **Übergabe.** Drei Knöpfe (§4).
5. **Aufnahme im Buch.** Die CI im Repo festgehalten baut den PR und lehnt formale Fehler
   ab. Der Halter prüft nach den Regeln der BUCH.md (§5.1) und nimmt an. Der Merge-Commit
   ist der Zeitpunkt der Hinterlegung. Danach gilt der Eintrag wie jeder andere:
   Auflösung, Beleg, Rangliste.

Doorway speichert nichts auf einem Server. Was im Browser des Hinterlegenden liegt
(Entwurf, §6.3), verlässt ihn nicht.

## 3. Formular: Schritte und Übersetzungsregeln

Der Hinterlegende sieht nie ein YAML-Feld. Das Formular übersetzt.

| Schritt | Frage | Wird zu |
|---|---|---|
| 1 Wer | Institution (Auswahl aus der Buchliste oder frei), Person oder Organ, das spricht | `institution`, `gesagt_von`, Zielbuch |
| 2 Was | Die Erwartung in eigenen Worten, ein bis drei Sätze | `zitat` |
| 3 Bis wann | Stichtag (Datum, in der Zukunft) | `frage` („… am <Stichtag>?"), `pruefung_am` = Stichtag + 1 Tag, `verfall_am` = `pruefung_am` + 6 Monate |
| 4 Woran erkennbar | Ja/Nein, oder Zahl mit Einheit, bei Zahl optional Toleranz | `typ`, `einheit`, `toleranz`, `wert` (bei Ja/Nein fest 1.00) |
| 5 Wo öffentlich | URL des Ortes, an dem das Ergebnis am Stichtag sichtbar sein wird | Textteil „Nachweis" |
| 6 Bedingung | Optional: Wovon hängt es ab, und bis wann muss das feststehen | Vermerk mit Frist |
| 7 Quelle | Optional: eigene öffentliche URL, unter der die Erwartung schon steht | `quelle`; sonst die URL der Datei im Zielbuch |

Feste Werte, die das Formular setzt und anzeigt, aber nicht verhandelt:

- `gesagt_am` und `hinterlegt_am` sind der Tag des Ausfüllens.
- `herkunft: hinterlegt`, `art: angekuendigt`, erste und einzige Prognose `von: <institution>`.
- `ausgang`, `aufgeloest_am`, `beleg_ausgang` sind `null`; `vermerke` enthält den
  Bedingungsvermerk oder ist leer.
- **Die id wird erzeugt, nicht gewählt:** `<kurz>-<jahr>-<mmdd><hhmm>`, zum Beispiel
  `koeln-2026-09051432`. `kurz` ist der Institutionsname in Kleinbuchstaben ohne
  Umlaute und Sonderzeichen, auf 20 Zeichen gekürzt; für Bücher aus der Liste der
  Ordnername. Eine doppelte id lehnt die CI des Buches ab (FORMAT §5.1).
- Teilerfüllung ist Nein, der Stichtag gilt wörtlich (FORMAT §2.2). Das Formular sagt
  das im Schritt 3.
- Nach dem Commit ändern sich nur noch `ausgang`, `aufgeloest_am`, `beleg_ausgang`,
  `vermerke` (FORMAT §1.3.3).

Textteile der Datei: **Kontext** (wer, worum es geht, Zielbuch, Datum), **Übersetzung**
(wie aus der Erwartung die Frage wurde, Stichtag, Regel „Teilerfüllung ist Nein"),
**Nachweis** (die URL aus Schritt 5 und der Satz, dass ein Schnappschuss dieses Ortes am
Prüftag ohne Artefakt als Beleg für Nein gilt), **Begründung <institution>** (der Satz
aus Schritt 2, „beim Wort genommen"). Bei Bedingung zusätzlich **Bedingung** mit Frist.

## 4. Ausgabe und Übergabe

Nach Schritt 7 zeigt die Seite die Datei vollständig an. Darunter drei Knöpfe:

1. **Als Pull Request anlegen.** Öffnet GitHubs Seite „neue Datei" im Zielbuch mit Pfad
   (`buecher/<ordner>/wetten/<id>.md`) und Inhalt vorausgefüllt
   (`https://github.com/<repo>/new/<zweig>/<pfad>?filename=<id>.md&value=<inhalt>`).
   Wer nicht Mitarbeiter des Repos ist, bekommt von GitHub Fork und PR angeboten. Der PR
   läuft unter dem GitHub-Konto des Hinterlegenden, nicht unter Doorway: Wer hinterlegt,
   bindet sich selbst. Doorway ist die Tür, nicht der Bote.
2. **Herunterladen.** Die Datei als `<id>.md`.
3. **Per Mail einreichen.** Öffnet das Mailprogramm mit der Einreichungsadresse des
   Zielbuchs (§5.2), Betreff „Hinterlegung <id>" und der Bitte, die heruntergeladene Datei
   anzuhängen. Der Dateiinhalt geht nicht in die Mail, weil Mailprogramme lange Texte
   abschneiden. Bücher ohne Einreichungsadresse zeigen den Knopf nicht.

**Zu lange Datei.** Der Inhalt reist in der URL. Die Seite berechnet die Länge der
fertigen PR-URL. Liegt sie über der Grenze `PR_URL_MAX`, ist Knopf 1 aus, und daneben
steht, dass Herunterladen und Mail bleiben. Kein stilles Abschneiden. Die Grenze wird in
der Umsetzung gegen GitHub gemessen und als Konstante mit Messdatum eingetragen; die
Freitexte des Formulars sind so begrenzt, dass ein gewöhnlicher Eintrag darunter bleibt.

Nach dem Klick auf Knopf 1 zeigt die Seite, was jetzt passiert: automatische
Formprüfung, Prüfung durch den Halter nach den vier Punkten der BUCH.md, Aufnahme durch
Merge, und dass der Merge-Zeitpunkt zählt. Mit Namen des Halters und Kontakt aus der
Buchliste.

Was die Seite nicht tut: keinen PR selbst öffnen. Das bräuchte ein Zugangstoken, also
einen Server oder ein fremdes Token in einer fremden Seite; beides ist ausgeschlossen.

## 5. Was im Repo festgehalten passieren muss

Alles vor dem Formular. Keine Formatänderung: `quelle` bleibt Pflicht-URL, `herkunft`
bleibt optionales Feld. §8.3 wird nicht ausgelöst.

### 5.1 Sammelbuch `buecher/hinterlegt/`

`BUCH.md` mit Titel „Hinterlegt", Halter Felix Lind, `kontakt` wie die Stadtbücher,
`einreichung` (Mailadresse, siehe 5.2), `sammelbuch: true`, `format: v1`. Im Text, datiert:

- Der Festpreis-Satz aus §1 Befund 6, wörtlich. Eine Abweichung ist entschieden (06.09.2026):
  im Sammelbuch heißt es „als Halter dieses Buches" statt „des Buches".
- Verfall-Regel des Halters: hinterlegte Einträge verfallen sechs Monate nach dem
  Prüfdatum; `verfall_am` steht in jeder Datei.
- „Der Halter dieses Buches hinterlegt nicht im eigenen Buch."
- **Wonach der Halter einen PR annimmt oder ablehnt**, vier Punkte:
  (1) Die Frage ist am Stichtag ohne Ermessen entscheidbar.
  (2) Der genannte öffentliche Ort ist heute schon erreichbar.
  (3) Eine Bedingung trägt eine Frist.
  (4) Die Quelle ist erreichbar und enthält das Zitat; ist die Quelle die Datei im Buch
  selbst, entfällt dieser Punkt.
  Was der Halter nicht prüft: ob die Erwartung klug ist.
- Aufnahme und Ablehnung geschehen als PR-Kommentar mit Nennung des Punktes; der
  Zeitpunkt der Hinterlegung ist der Merge-Commit.

Ob der Generator ein Buch ohne Einträge baut, prüft die Umsetzung als erstes; falls
nicht, wird das im Generator behoben (kein Formatthema).

Eine Institution, die später ein eigenes Buch bekommt, behält ihre Einträge im
Sammelbuch. Nichts wird verschoben (FORMAT §1.3.3).

### 5.2 Buchliste `buecher.json`

Der Generator (`alle`) erzeugt neben `alle.json` eine `buecher.json`, je Buch:

```json
{
  "ordner": "koeln",
  "titel": "Köln gegen Köln",
  "institution": "Stadt Köln",
  "halter": "Felix Lind",
  "kontakt": "https://belegbar.eu",
  "einreichung": "…@…",
  "repo": "Felix3c/festgehalten",
  "zweig": "main",
  "pfad": "buecher/koeln/wetten",
  "sammelbuch": false
}
```

Neue optionale Felder in BUCH.md: `institution` (Name der gemessenen Stelle, für
Stadtbücher der Stadtname; fehlt es, ist das Buch im Formular nicht als Ziel wählbar),
`einreichung` (Mailadresse), `sammelbuch: true` (genau einmal in der Liste). `repo`,
`zweig` und `pfad` leitet der Generator aus dem Aufruf ab (Parameter `--repo`, Zweig aus
Git, Pfad aus dem Ordner). Der Generator prüft `einreichung` als Mailadresse und dass
höchstens ein Buch `sammelbuch: true` trägt.

Doorway nimmt eine Kopie nach `site/daten/buecher.json` auf, ergänzt um `stand` (Datum
der Kopie). Ein neues Buch heißt: Generator läuft, Datei kopieren, ein Commit in Doorway.
Kein Laden zur Laufzeit; sechs Bücher in einem Repo rechtfertigen keinen Fehlerpfad.

### 5.3 Prüf-Workflow für Pull Requests

Neuer Workflow `pruefen.yml`, Auslöser `pull_request`, Rechte nur `contents: read`.
Läuft `pytest` und `python -m wettbuch alle buecher site`; ein Fehler des Generators
(FORMAT §5.1: Dateiname und Feld) lässt den Check rot werden. Kein Deploy. `pages.yml`
bleibt unverändert und läuft nur bei Push.

## 6. Prüfung, Entwurf, Status

### 6.1 Aufbau im Code

Zwei neue Dateien in `site/`: `hinterlegen.html` und `hinterlegen.mjs`. Das Modul ist
rein: `uebersetzen(eingaben, buecher, jetzt)` gibt `{ datei, id, zielbuch, fehler }`
zurück, ohne DOM. Dazu `prUrl(zielbuch, id, datei)` und `urlZuLang(url)`. Die Seite
hängt die Felder an das Modul und rendert. Gleiche Bauart wie `regeln.mjs` und `app.js`,
gleiches `stil.css`. `index.html` bekommt einen Link „Selbst hinterlegen".

### 6.2 Prüfung im Browser

Das Modul prüft dieselben Regeln, die `pruefen.py` im Generator kennt, soweit sie eine
neue Datei betreffen: Pflichtfelder, id-Muster `^[a-z0-9][a-z0-9-]*$`, Datumsformat,
`quelle` und Nachweis-Ort als http(s)-URL, Stichtag nach heute, `wert` 1.00 bei
Ja/Nein, `einheit` bei Zahl, `toleranz` als Zahl. Dazu die Formularregeln: Längen der
Freitexte, Bedingung nur mit Frist. Fehler stehen am Feld, in Worten, ohne YAML-Namen.
Der Rundlauf-Test (§7.2) hält beide Regelsätze zusammen.

### 6.3 Entwurf lokal

Jede Eingabe wird im Browser-Speicher (`localStorage`) des Hinterlegenden abgelegt und
beim nächsten Öffnen wiederhergestellt: „Entwurf vom <Datum> wiederhergestellt." Ein
Knopf „Entwurf löschen" leert ihn. Die Seite sagt an derselben Stelle wie der Spiegel,
dass nichts den Browser verlässt, und warnt, dass der Entwurf auf einem geteilten Rechner
für andere sichtbar bleibt. Der Speicher kann fehlen oder gesperrt sein; dann arbeitet die
Seite ohne Entwurf und sagt das.

### 6.4 Status per id

Ein Feld „id eingeben" auf derselben Seite. Eine Leseabfrage der statischen Datei
`https://felix3c.github.io/festgehalten/<ordner>/wettbuch.json` des Zielbuchs (das
Buch ergibt sich aus dem Präfix der id, sonst werden alle Bücher der Liste abgefragt).
Ist die id drin: „aufgenommen" mit Link auf die Eintragsseite. Sonst: „noch nicht
aufgenommen" mit Link auf die PR-Liste des Repos. Schlägt die Abfrage fehl, sagt die
Seite das und zeigt denselben Link. Kein GitHub-API, keine Anmeldung, kein Ratenlimit.
Das ist der einzige Zugriff der Seite auf eine fremde Origin, und er geschieht nur auf
Klick.

## 7. Tests

1. **Modul.** `node site/pruefung.mjs` wie heute, erweitert: eine gültige Eingabe ergibt
   eine gültige Datei mit erwarteten Feldern; jede Regel aus §6.2 hat einen Fehlerfall;
   id-Bildung mit Umlauten und langen Namen; Zielbuch-Wahl (Liste, frei, Sammelbuch);
   `verfall_am`-Rechnung über Jahresgrenzen; `urlZuLang` an der Grenze.
2. **Rundlauf.** Ein pytest-Test in Doorway erzeugt per Node die Beispieldatei, liest sie
   mit dem Lader des festgehalten-Generators und ruft dessen `pruefen` auf: null Fehler.
   Der Generator kommt als Test-Abhängigkeit, **auf einen Commit gepinnt**
   (`festgehalten @ git+https://github.com/Felix3c/festgehalten@<sha>`). Ein Sprung des
   Pins ist eine bewusste Änderung, kein Zufall.
3. **Abnahme durch Felix.** Ein erfundener Fall, durchgeklickt bis zum PR im Sammelbuch.
   PR-Titel beginnt mit „Probelauf". Der PR wird geschlossen, nicht gemerged. Erst danach
   ist Teil 3 fertig.

`python -m pytest -q` (Teil 1, 128 Tests) und `node site/pruefung.mjs` bleiben grün.

## 8. Reihenfolge der Umsetzung

1. festgehalten: Sammelbuch, `buecher.json`, `pruefen.yml`; Generator baut leeres Buch.
2. Doorway: `hinterlegen.mjs` mit Tests (Modul, Rundlauf).
3. Doorway: `hinterlegen.html`, Entwurf, Status, Link von `index.html`.
4. Messung `PR_URL_MAX` gegen GitHub, Konstante eintragen.
5. Abnahme (Probelauf-PR), dann Statusdateien.

## 9. Nicht in Teil 3

Bearbeiten nach dem Commit. Werkzeuge für den Halter. Ein zweiter Halter oder ein
Buch außerhalb des Repos festgehalten. Preise über null. Felix' eigener Eintrag
(`lind-2026-001` bleibt Probe). Ein PR, den Doorway selbst öffnet. Konten, Server,
Speicherung außerhalb des Browsers des Hinterlegenden. Prognosen anderer als der
Institution im hinterlegten Eintrag; Computer und Halter kommen wie bei zitierten
Einträgen später durch den Halter dazu.
