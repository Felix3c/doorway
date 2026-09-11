# Doorway — Nächste Schritte

**Stand:** 11.09.2026, spät abends (Plan 2 komplett: PR #1 gemerged, `hinterlegen.html` live, Probelauf bis zum PR #3 in festgehalten mit grünem Check, PR geschlossen)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`; **Teil 3: `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`**
**Phase:** Teil 1, 2 und 3 veröffentlicht. Teil 3 ist abgenommen (Task 7 erledigt). Es gibt keinen laufenden Plan.

---

## Leitsatz

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Übergeordnete These: `~/THESE.md`. Prüffrage für jedes Feature: *nachprüfbarer oder nur bequemer?*

## Zielbild (01.09.2026, aus ~/GUARD.md Ebene 3 und FORMAT.md §8.4)

**Doorway ist der Zugang zu allem, was Bindung belohnt.** Wer etwas will, das andere vergeben
— Geld, Genehmigung, Legitimität — hinterlegt vorab, datiert und öffentlich, was er erwartet.
Doorway baut die Tür für diese Hinterlegung und die Werkzeuge für die Seite, die vergibt.
Die Stadt ist das Produkt, nicht der Kunde. Kundenliste und Regel `herkunft: hinterlegt`:
Commit ab2ad9a bzw. FORMAT.md §8.4.

## Wo wir stehen

- **Live:** https://felix3c.github.io/doorway/ — Spiegel, Panel, Nein-Register, Quellen.
  An der veröffentlichten Seite wurde seit der Abnahme am 01.09. nichts geändert.
- **Plan 1 (festgehalten) gemerged** (PR #1, `f848d80`, 08.09.). Buchliste live mit sechs
  Einträgen, Sammelbuch `hinterlegt` mit `einreichung: hinterlegt@belegbar.eu`.
- **Plan 2 auf dem Zweig `hinterlegen`** in `~/doorway`, **nicht gepusht, kein Upstream.**
  Commits über `master` hinaus (in dieser Reihenfolge): `65c050e`, `8922b6f`, `f23a449`,
  `013e648`, `f80e9a7` (docs), `35ed74e` (Task 3), `82fb3fd` (Task 4), `126e28c` + `b618c42`
  (Task 5 + Fix-Runde), `f8d65bd` (Task 6). Jeder Task hat ein sauberes Review im Ledger.
  - Task 3: `prUrl`, `urlZuLang`, `mailUrl`, `statusUrl`, `prListeUrl`, `FESTGEHALTEN_SEITE`.
  - Task 4: `tests/test_hinterlegen_rundlauf.py` — die erzeugte Datei besteht `lesen` und
    `pruefen` des echten Generators. **`pip install -e ".[dev]"` wurde bewusst nicht
    ausgeführt** (Ruling D): `festgehalten` ist als Editable-Install aus `~/wettbuch`
    vorhanden, und dort arbeitete ein anderer Tab. Der Pin steht in `pyproject.toml`.
  - Task 5: `site/hinterlegen.html`, `site/hinterlegen-seite.js`, Link in `index.html`,
    CSS nur `.optionen a.button` und erweiterter Feld-Selektor (+ `:focus`). Durchklick
    lokal mit chrome-devtools bestanden: Fehler am Feld, Vorschau, Entwurf, PR-/Download-/
    Mail-Link, Status mit echter Köln-id („aufgenommen", Link `…/koeln/wette/<id>.html`).
  - Task 6: `PR_URL_MAX = 6400`, `GRENZEN.zitat = 400`, `bedingung = 200`, `maxlength`
    angeglichen. Messung per curl gegen github.com **ohne Login**: bis 6905 Zeichen
    HTTP 302 (Login-Umleitung), ab 7043 HTTP 500, ab 12011 HTTP 414. Ob GitHub im
    eingeloggten Zustand bei ~6400 Zeichen den Inhalt wirklich vorbefüllt, ist
    **ungeklärt** — das prüft Felix im Probelauf.
- **Final-Review (opus) über `65c050e..f8d65bd`: „Ready with fixes".** Ein Critical:
  `yamlText` escaped keine Zeilenumbrüche — Enter im Zitat wird vom YAML zu einem Leerzeichen
  gefaltet, eine `---`-Zeile macht die Datei unlesbar. Dazu sechs Importants (unquoted
  `quelle`, fünf Fehlerkästen beim leeren Erstaufruf, Text bei fehlender Buchliste
  verspricht zu viel, `aria-live` auf der ganzen Vorschau, Rundlauf nur für `ja_nein`,
  leerer Entwurf wird gespeichert und als „wiederhergestellt" gemeldet).
- **Fix-Welle dazu war beim Umsetzer, als die Sitzung endete.** Erwarteter Commit:
  `fix: YAML-Escapes für Zeilenumbrüche, ehrliche Hinweise, Rundlauf für punkt (Final-Review)`
  mit Bericht `.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/final-fix-report.md`.
  Beim Sitzungsende waren `site/hinterlegen.mjs` und `site/hinterlegen.pruefung.mjs`
  geändert, aber nicht committet. Ob der Commit noch gelandet ist: `git log --oneline
  f8d65bd..HEAD` — leer heißt, die Fix-Welle ist unvollständig und wird mit dem Bericht
  (falls vorhanden) und dem Ledger neu aufgesetzt.
- **Gemessen heute (vor der Fix-Welle):** `node site/hinterlegen.pruefung.mjs` „ok: 12
  Fälle", `node site/pruefung.mjs` grün, `python -m pytest -q` 129 grün (mit dem
  vorhandenen `wettbuch`-Install; ohne dev-Extra würde der Rundlauf still übersprungen).
- **Ledger** mit allen Rulings A–P, Findings und vertagten Kleinigkeiten:
  `.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/progress.md` (gitignored).
  Wichtigste neue Rulings: D (kein pip install), E/H (CSS-Umfang), G (Grenzen aus der
  Messung), M (ehrlicher Text statt hart kodiertem Fallback-Buch), N (`istZahl` nur mit
  Punkt), O (Umfang der Fix-Welle: #1–#7, #12, #14; offen bleiben #8, #9, #13, #15, #16),
  P (Plan Task 6 Step 2 wörtlich nicht erfüllbar, 400/200 bleibt; `#danach` vor dem Klick).
- **Lokaler `master`** hat einen ungepushten Docs-Commit `75ec62e`; der Zweig enthält ihn.
- Chrome-Erweiterung war heute nicht verbunden; Browserarbeit lief über chrome-devtools
  (eigenes Chrome ohne GitHub-Login). `gh` fehlt weiterhin.

## Nachtrag später am Abend

- **Fix-Welle gelandet:** `d4cb2b9` fixt #1–#7, #12, #14 (yamlText escaped `\n`/`\r`/`\t`,
  `quelle` quoted, `istZahl` nur Punkt, `--beispiel punkt`, Rundlauf parametrisiert, berührte
  Felder, kein leerer Entwurf, ehrlicher Buchlisten-Hinweis, `aria-live` auf Statuszeile).
  Gemessen danach: „ok: 13 Fälle", `pruefung.mjs` grün, `python -m pytest -q` 130 grün.
- **Scoped Re-Review sauber**, alle zehn Findings adressiert. Neuer deferred minor: ein Entwurf
  mit nur gewähltem Typ „Zahl" und sonst leeren Feldern wird nicht gespeichert.
- **Zweig gepusht:** `origin/hinterlegen` = `d4cb2b9`, Upstream gesetzt. Kein PR angelegt
  (kein `gh`, kein GitHub-Login in der Session).

## Abnahme (Task 7, 11.09. spät, auf Felix' Bitte durch die Session in seinem Chrome)

- **PR #1 in Doorway** angelegt und als Merge-Commit `80863ee` gemerged (14 Commits, 13 Dateien).
  Pages war nach etwa einer Minute live: https://felix3c.github.io/doorway/hinterlegen.html
- **Probelauf:** „Probelauf e.V." auf der Live-Seite, id `probelauf-e-v-2026-09111845`, PR-URL
  2213 Zeichen. GitHub „New file" war vollständig vorbefüllt (Dateiname und alle 40 Zeilen).
  Commit auf Zweig `probelauf-doorway-teil-3`, PR #3 in festgehalten, Check `pruefen`
  completed/success, PR geschlossen, nicht gemerged.
- **Status auf der Seite:** Probelauf-id → „Noch nicht aufgenommen" mit Link auf die PR-Liste;
  `koeln-2025-001` → „aufgenommen" mit Link auf `koeln/wette/koeln-2025-001.html`.
- Der Probelauf-Entwurf wurde im Browser wieder gelöscht.
- **Weiterhin ungemessen:** ob GitHub bei einer URL nahe `PR_URL_MAX` (6400) noch vorbefüllt.
  Der Probelauf lag bei 2213 Zeichen. Wer es wissen will: Zitat 400 und Bedingung 200 Zeichen
  mit vielen Umlauten füllen (URL etwa 5800) und Knopf 1 drücken.

## Nächster konkreter Schritt

**Aufräumen und den ersten echten Eintrag abwarten.** Konkret: Zweig `hinterlegen` in
Doorway und Zweig `probelauf-doorway-teil-3` in festgehalten auf GitHub löschen (beide gemerged
bzw. geschlossen), dann den Ledger-Workspace `.superpowers/sdd/2026-09-05-…` entfernen
(Ruling Q, Merge ist durch). Die vertagten Kleinigkeiten aus dem Final-Review (#8, #9, #13,
#15, #16, Entwurf nur mit Typ) stehen im Ledger — vor dem Löschen in ein Issue oder in diese
Datei übernehmen, wenn sie erhalten bleiben sollen.

## Wartet auf Felix

- **Alias `hinterlegt@belegbar.eu` bei ImprovMX anlegen** — steht im Sammelbuch, ohne Alias
  laufen Mails ins Leere. Der Mail-Knopf auf der Seite zeigt schon dorthin.
- **Erster echter hinterlegter Eintrag** (nicht Felix' eigener): wem die Seite gezeigt wird.
- Später: `pip install -e ".[dev]"` in `~/doorway`, sobald `~/wettbuch` frei ist (ersetzt
  den Editable-Install durch den gepinnten Stand `f848d80`).

## Blocker

Keine. (Speicher war heute knapp: Hintergrundprozesse wurden vom System beendet.
Keine Dauerprozesse starten, Browserseiten schließen.)

## Wie eine neue Session hier einsteigt

1. Diesen Stand lesen, dann den Ledger (Verlauf ab „11.09.").
2. `git branch --show-current` muss `hinterlegen` sagen; sonst `git checkout hinterlegen`.
3. `git log --oneline f8d65bd..HEAD` und `git status` — entscheidet, ob die Fix-Welle
   committet ist.
4. `node site/pruefung.mjs` und `python -m pytest -q` als Ausgangslage.
5. Nichts an der Seite ändern, was nicht in der Spec steht; Abweichungen ins Ledger.
6. `~/wettbuch` nicht anfassen, wenn dort ein anderer Tab arbeitet (heute: Zweig
   `weitsicht`, ungesicherte Dateien).
