# Doorway — Nächste Schritte

**Stand:** 2026-08-26 (Historie bereinigt, Repo-Entscheidung gefallen; Kill-Kriterium vom 25.08.: v1 geht NICHT live)
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

## Nächster konkreter Schritt

**Stufe 2 überarbeiten, damit das Intervall bei dünner Datenlage ehrlich bleibt:** In `src/doorway/basisrate.py` ein Mindestintervall einführen, wenn weniger als drei Vorjahre vorliegen — Kandidat ist die über alle Elemente beobachtete Regimeschwankung statt der elementeigenen. Danach `doorway kill-kriterium` erneut laufen lassen. Erst wenn beide Hürden halten, wird Teil 2 geplant. Hält Hürde 2 auch dann nicht, ist die Corona-Lücke 2020 (IFG-Anfrage, §7) der Weg, nicht eine weichere Hürde.

## Wartet auf Felix

- **Remote anlegen:** privates GitHub-Repo (entschieden 26.08., siehe unten). Die Historie ist seit 26.08. frei von Klarnamen (geprüft: 0 Treffer über alle Commits). Push ist damit freigegeben — braucht nur noch dein GitHub-Login.

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
