# Doorway — Nächste Schritte

**Stand:** 11.09.2026, Nacht (Teil 3 live und abgenommen; Aufräumen bis auf drei gesperrte Befehle erledigt)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel = Leitsatz); Teil 2: `docs/superpowers/specs/2026-08-27-doorway-teil-2-design.md`; Teil 3: `docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md`
**Phase:** Teil 1, 2 und 3 veröffentlicht. Kein Plan läuft. Doorway wartet auf den ersten echten hinterlegten Eintrag.

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

**Live:** https://felix3c.github.io/doorway/ — Spiegel, Panel, Nein-Register, Quellen (Teil 1 + 2,
abgenommen 01.09.) und seit heute https://felix3c.github.io/doorway/hinterlegen.html (Teil 3).

**Git:** Zweig `master`, sauber, nichts ungepusht (Stand: `git log -1`).
Merge-Commit von Teil 3: `80863ee` (PR #1, 14 Commits, 13 Dateien).

**Teil 3 ist fertig.** Der Hinterlegungs-Pfad nimmt sieben Antworten, erzeugt daraus eine Datei
im festgehalten-Format v1 und übergibt sie als vorbefüllten Pull Request, Download oder Mail.
Nichts verlässt den Browser außer der Statusabfrage auf Klick.

- `site/hinterlegen.mjs` — reines Modul: id-Bildung, Eingabeprüfung, Dateierzeugung, Adressen.
- `site/hinterlegen.pruefung.mjs` — 13 Node-Fälle, eingehängt in `site/pruefung.mjs`;
  `--beispiel [punkt]` gibt die Beispieldatei aus.
- `tests/test_hinterlegen_rundlauf.py` — die erzeugte Datei besteht `lesen` und `pruefen` des
  echten festgehalten-Generators, in beiden Varianten (`ja_nein`, `punkt`).
- `site/hinterlegen.html` + `site/hinterlegen-seite.js` — Formular, Vorschau, Entwurf, Status.
- `site/daten/buecher.json` — Kopie der Buchliste, Stand 2026-09-08, heute geprüft: byteidentisch
  mit der Live-Liste auf festgehalten.

**Gemessen in dieser Sitzung:** `node site/hinterlegen.pruefung.mjs` „ok: 13 Fälle",
`node site/pruefung.mjs` grün, `python -m pytest -q` 130 grün ohne Warnungen.
Die 130 setzen voraus, dass `wettbuch` importierbar ist; ohne das dev-Extra wird der Rundlauf
still übersprungen.

**Grenzen (Ruling G, per curl gegen github.com ohne Login gemessen):** `PR_URL_MAX` 6400,
`GRENZEN.zitat` 400, `bedingung` 200. Rohdaten: bis 6905 Zeichen HTTP 302, ab 7043 HTTP 500,
ab 12011 HTTP 414.

**Abnahme (Task 7), heute durch die Session in Felix' Chrome auf seine Bitte:**

- PR #1 in Doorway angelegt und gemerged; Pages war nach etwa einer Minute live.
- Probelauf auf der Live-Seite: „Probelauf e.V.", id `probelauf-e-v-2026-09111845`,
  PR-URL 2213 Zeichen. GitHub „New file" war vollständig vorbefüllt (Dateiname und alle
  40 Zeilen). Commit auf Zweig `probelauf-doorway-teil-3`, daraus PR #3 in festgehalten.
- Check `pruefen` in festgehalten: completed/success. PR #3 geschlossen, **nicht** gemerged
  (per API bestätigt: state closed, merged false, 11.09. 16:50 UTC).
- Statusabfrage auf der Seite: Probelauf-id → „Noch nicht aufgenommen" mit Link auf die
  PR-Liste; `koeln-2025-001` → „aufgenommen" mit Link auf `koeln/wette/koeln-2025-001.html`.
- Der Probelauf-Entwurf wurde im Browser wieder gelöscht.

**Ungeklärt:** ob GitHub bei einer URL nahe `PR_URL_MAX` (6400) noch vollständig vorbefüllt.
Der Probelauf lag bei 2213 Zeichen. Wer es prüfen will: Zitat 400 und Bedingung 200 Zeichen mit
vielen Umlauten füllen (URL dann etwa 5800) und Knopf 1 drücken.

**Review-Spuren.** Jeder Task hat ein eigenes Review, dazu ein Final-Review über den ganzen
Zweig (fand einen echten Fehler: `yamlText` escapte keine Zeilenumbrüche, ein Enter im Zitat
hätte YAML gefaltet, eine `---`-Zeile die Datei unlesbar gemacht), eine Fix-Welle `d4cb2b9` und
ein sauberes Re-Review. Die Rulings A–Q sind seit heute Nacht als **§10 der Teil-3-Spec**
gesichert. Der Ledger `.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung/` (gitignored)
liegt noch auf der Platte, weil die Session ihn nicht löschen durfte.

**Vertagte Kleinigkeiten** aus allen Reviews, bewusst nicht gefixt, stehen jetzt in
`docs/vertagt.md` (zehn Punkte, dazu die ungemessene Vorbefüllung nahe 6400 Zeichen).

## Nächster konkreter Schritt

**Drei Löschbefehle, die nur Felix ausführen kann.** Der Auto-Modus sperrt sie für die
Session (Zweige löschen, Ordner löschen). In Tab 8 mit `!` davor, jeder einzeln:

```
git -C ~/doorway branch -d hinterlegen && git -C ~/doorway push origin --delete hinterlegen
git -C ~/doorway push https://github.com/Felix3c/festgehalten.git --delete probelauf-doorway-teil-3
rm -rf ~/doorway/.superpowers/sdd/2026-09-05-doorway-teil-3-hinterlegung
```

Geprüft: `hinterlegen` ist vollständig in `master` (Merge `80863ee`); PR #3 in festgehalten
ist geschlossen; der Ledger-Inhalt steht in Spec §10 und `docs/vertagt.md`. Der zweite Befehl
fasst `~/wettbuch` nicht an. Danach ist Doorway ohne offene Aufgabe.

## Wartet auf Felix

- **Alias `hinterlegt@belegbar.eu` bei ImprovMX anlegen.** Der Mail-Knopf auf der Seite zeigt
  schon dorthin; ohne Alias laufen Mails ins Leere.
- **Erster echter hinterlegter Eintrag**, nicht von Felix selbst: wem die Seite gezeigt wird.
- Später, ohne Eile: `pip install -e ".[dev]"` in `~/doorway`, sobald `~/wettbuch` frei ist.
  Heute bewusst nicht ausgeführt (Ruling D), weil dort ein anderer Tab arbeitete und der Befehl
  dessen Editable-Installation durch den gepinnten Stand `f848d80` ersetzt hätte.

## Blocker

Keine.

## Wie eine neue Session hier einsteigt

1. Diesen Stand lesen. Offene Kleinigkeiten in `docs/vertagt.md`, Entscheidungen in Spec §10.
2. `git branch --show-current` muss `master` sagen, Arbeitsbaum sauber.
3. `node site/pruefung.mjs` und `python -m pytest -q` als Ausgangslage.
4. Nichts an der Seite ändern, was nicht in der Spec steht; Abweichungen in die Spec schreiben.
5. `gh` ist auf diesem Rechner nicht installiert. GitHub lesend über die API (curl), schreibend
   über `git push` oder die Chrome-Werkzeuge.
6. `~/wettbuch` nicht anfassen, wenn dort ein anderer Tab arbeitet.
