# Doorway — Nächste Schritte

**Stand:** 2026-08-26 (Mindestintervall gebaut, viertes Urteil: Hürde 2 reißt strukturell an 2019/2021; Historie bereinigt; Repo wird privat)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Präambel mit Leitsatz seit 25.08.)
**Plan Teil 1:** `docs/superpowers/plans/2026-08-25-doorway-ernte-und-urteil.md` — alle 13 Tasks erledigt
**Phase:** Urteil gefällt. Stufe 2 muss überarbeitet werden, bevor Teil 2 (Spiegel, Web, öffentliches Register) überhaupt geplant wird.

---

## Leitsatz (25.08.2026)

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Doorway ist nicht "Förderung finden", sondern "Ablehnung nachprüfbar machen". Übergeordnete These: `~/THESE.md`. Prüffrage für jedes Feature: *nachprüfbarer oder nur bequemer?*

## Wo wir stehen

**Gebaut (Git `master`, 108 Tests grün, Arbeitsbaum sauber, kein Remote):**

- `doorway laden` — sechs Landtagsdokumente, SHA-256-Lock; Prüfsummen identisch mit den Kopien vom 24.08.
- `doorway ernten` — Korpus 4.605 Entscheidungen (1.296 aus 2025, 3.309 aus 2018/2019), Register 78 Zeilen, 0 Konflikte, jede Zeile mit Herkunft
- `doorway prognose "<Vorhaben>"` — zweistufig gerechnet, einstufig angezeigt (§12.4)
- `doorway kill-kriterium` — beide Hürden aus §14.2, Rückgabewert 0/1
- Selbstwiderspruchstest (§14.1) läuft: Vorl 18/5027 sagt 598/329 im Text, zählt 596/330 in der Anlage

**Das Urteil (dreimal gemessen, das letzte gilt):**

```
Huerde 1  falsche Absagen   vereinseigene Ausstattung 0/22 = 0.0%   bestanden
Huerde 2  Kalibrierung      5 von 15 Vorhersagen ausserhalb          GERISSEN
ERGEBNIS: v1 geht NICHT live.
```

Alle fünf Fehlschläge haben dieselbe Ursache: der Sprung 2019→2021 (Fonds 26→6 %, Scheck 40→24 %, Werkstatt 54→13 %, Zeugnis 55→17 %) und Scheck 2019, wo nur ein Vorjahr vorliegt und das Intervall deshalb nur der Stichprobenfehler (±2,6 %) ist. Für 2025 liegen alle fünf Elemente im Intervall.

**Gegen die Quellen gelernt (alles im Extraktor korrigiert, nie im Test; Details in den Commit-Nachrichten):**

- Drs 17/9738 ist **nicht** anonymisiert, anders als der Plan annahm: die Antragsteller-Spalte enthält Vereinsnamen und mindestens eine Privatperson. Typ wird jetzt beim Extrahieren auf die elf erlaubten Werte abgebildet (281 Kommunen, 25 "unbekannt").
- 11 Vorhabentitel 2025 tragen den Vereinsnamen → gestrichen; 3 Titel entfallen ganz.
- Regel "vereinseigene Ausstattung" riss mit 41/66 = 62 %, weil 41 von 44 *Vereinsfahnen* bewilligt wurden → Muster auf `trikot|uniform` verengt (0/22).
- Register hatte für 2018/19 keine landesweite Zeile → Summenzeile "über alle" ergänzt (ohne sie sagte die Kalibrierung 2025 allein aus 2021 vorher).
- Quellfehler, nie geraten: "29.02.2019", "13.09.20218", zwei Antragsdaten in einer Zelle (letztes zählt), 5 Antragsjahre nach dem Entscheidungsjahr (kein Förderjahr), Zeile 644 "Overath" in der Elementspalte (behalten als "unbekannt").

## Viertes Urteil (26.08.2026, nach Mindestintervall in Stufe 2)

Untergrenze eingebaut: bei weniger als drei Vorjahren gilt die größte Schwankung, die irgendein Element bis dahin gezeigt hat (`basisrate.uebergreifende_schwankung`). Wirkung: Scheck 2021 ±4,4 → ±7,4 %, Preis 2021 ±2,7 → ±7,4 %. **Hürde 2 reißt trotzdem, 5 von 15** — und zwar strukturell:

- **2019:** erstes Jahr aller Elemente ist 2018; niemand hat zwei Jahre, also gibt es keine Vergleichsschwankung. Scheck 2019 bleibt bei ±2,6 % und liegt 3 Punkte daneben.
- **2021:** Fonds 26→6 %, Scheck 40→24 %, Werkstatt 54→13 %, Zeugnis 55→17 %. Der Einbruch nach der Corona-Lücke ist aus 2018/19 nicht vorhersehbar, mit keinem Intervall, das noch eine Aussage wäre.
- **2025:** alle fünf Elemente im Intervall.

Der Befund: Die Prognose funktioniert, sobald sie drei Jahre kennt. Die Hürde, wie sie in §14.2 steht ("jede Klasse im Backtest innerhalb ihres Intervalls"), verlangt aber auch Treffer in Jahren, in denen es nichts zu wissen gab.

## Nächster konkreter Schritt

**Entscheidung von Felix** (siehe unten), dann entweder §14.2 präzisieren oder die IFG-Anfrage für 2020 stellen. Keine Programmierarbeit, bevor das entschieden ist — sonst wird die Hürde stillschweigend gelockert, und genau das verbietet der Plan.

## Wartet auf Felix

- **Hürde 2 — präzisieren oder Daten holen?** Zwei ehrliche Wege, ein unehrlicher:
  - *Präzisieren:* Die Kalibrierung zählt nur Vorhersagen, denen mindestens drei belegte Vorjahre zugrunde liegen; 2019 und 2021 wären dann keine Prüfjahre, sondern Lernjahre, und das Panel zeigt für Kombinationen mit weniger Jahren keine Zahl. Das ist eine Änderung an §14.2 und gehört datiert in die Spec.
  - *Daten holen:* IFG-Anfrage für 2020 (und 2022). Mit 2020 sähe die Prognose den Einbruch ein Jahr früher. Ein Monat Frist, 10–500 € Risiko. Ändert nichts an 2019.
  - *Unehrlich wäre:* das Intervall so weit aufblasen, bis 2021 hineinfällt. Dann hält die Hürde, aber die Zahl sagt nichts mehr.
- **Remote anlegen:** privates GitHub-Repo (entschieden 26.08.). Historie seit 26.08. frei von Klarnamen (0 Treffer über alle Commits). Push ist freigegeben — braucht nur dein GitHub-Login.

## Entschieden am 2026-08-26

- **Git-Historie bereinigt.** Das Golden File `golden/drs-17-9738.json` trug in den Commits vom 25.08. den Klarnamen einer Privatperson (Antragsteller-Spalte der Drs 17/9738). Alle Commits per `filter-branch` umgeschrieben, Sicherungs-Refs gelöscht, `gc --prune=now`; `git log -p --all` findet den Namen nicht mehr. Hashes ab dem Extraktor-Commit haben sich geändert (alt `2647a73`, neu `1344894`).
- **Repo wird privat, Korpus bleibt versioniert.** `daten/korpus.jsonl` ist intern (§13.1); ein privates Repo veröffentlicht nichts, und der Korpus bleibt als Diff nachvollziehbar. Öffentlich wird später nur das Register.
- **Stufe 2: Mindestintervall zuerst,** IFG-Anfrage 2020/2022 erst, wenn Hürde 2 danach immer noch reißt.

## Blocker

Keiner. Alles Weitere ist Entscheidung, nicht Hindernis.

## Wie eine neue Session hier einsteigt

1. Spec lesen (Präambel zuerst), dann diesen Wegweiser.
2. `python -m pytest -q` — muss 108 grün liefern. `PYTHONPATH=src python -m doorway.cli kill-kriterium` zeigt das Urteil.
3. Nicht mit Teil 2 anfangen. Der Plan sagt: Reißt eine Hürde, wird Stufe 1/2 überarbeitet, nicht die Oberfläche gebaut.
