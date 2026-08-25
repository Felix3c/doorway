# Doorway — Nächste Schritte

**Stand:** 2026-08-25 (Wende entschieden: Doorway macht Ablehnungen nachprüfbar; Flaggschiff bestätigt)
**Führendes Dokument:** `docs/superpowers/specs/2026-08-24-doorway-design.md`
**Recherchebericht:** `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`
**Phase:** Ausführung Teil 1 (Ernte und Urteil). Design und Plan stehen; Leitsatz siehe „Die Wende“ unten.

---

## Entschieden am 2026-08-25 — die Wende

**Doorway ist nicht "Förderung finden", sondern "Ablehnung nachprüfbar machen".** Der Leitsatz steht ab jetzt über Spec, Plan und jedem Task:

> Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?

Hintergrund ist die gemeinsame These vom 25.08.: Intelligenz wird kostenlos, knapp bleibt **Haftung** — dass eine Aussage über Zeit an jemanden gebunden ist. Doorway ist das Projekt, in dem diese These zuerst konkret wird: Die Verwaltung hat ihre Ablehnungsgründe bereits in Vorlagen festgeschrieben; Doorway bindet sie, datiert sie und macht sie prüfbar. Das Nein-Register ist der Kern, Spiegel und Prognose sind Konsequenzen daraus, nicht umgekehrt.

**Was die Wende konkret ändert:**

- **Reihenfolge.** Beleg und Register haben Vorrang vor Spiegel und Prognose. Wenn im Plan ein Task beides berührt, gewinnt der Beleg. Die Prognose darf nie etwas behaupten, das nicht auf eine Fundstelle zurückführt (steht in §12, gilt jetzt als Leitplanke, nicht als Feature).
- **Test für jedes Feature.** Neben "darf keine Abrechnung werden" (Leitplanke oben) gilt: *Macht dieses Feature eine Entscheidung nachprüfbarer, oder nur bequemer?* Nur-bequem wird nachrangig.
- **Doorway bleibt Flaggschiff.** Kein fünftes "Infrastruktur"-Projekt. Die gemeinsame Schicht (Zeitstempel/Ledger, Herkunft, Scoring Rule) wird erst dann herausgezogen, wenn belegbar.eu und Doorway dieselbe Schicht nachweislich brauchen — nicht vorher.
- **Zeitbudget aufgelöst:** `messen` und Nährboden sind geparkt, bis Doorway ein Amt tatsächlich gebunden hat (erstes veröffentlichtes Register mit Fundstellen). belegbar.eu läuft im Wartungsmodus weiter.

## Wo wir stehen

**Entschieden und in der Spec festgehalten:**

- Die These (das Geheimnis): Stillstand ist ein Auszahlungsproblem, kein Charakterproblem. Schwellen sortieren die aus, die es versuchen würden — das sieht von außen aus wie Faulheit, ist aber Aussperrung.
- Name: **Doorway**. Anspruch: "Open the door of the future." Datensatz: **Das Nein-Register**.
- Was v1 tut: Spiegel, Prognose, Beleg, Register. Was v1 **nicht** tut: keine Antragstexte, keine Beratung, kein Premium, keine Behördenbewertung.
- Das Register ist **aggregiert** (je Programm und Jahr), niemals namentlich.
- Rollenteilung: Körper = die Domäne, Herz = Proper Scoring Rule aus `messen`, Gesetz = Belegbarkeits-Disziplin aus belegbar.eu. Code wird nie verschmolzen, nur die Mechanik übernommen.
- Leitplanke: Doorway darf keine Abrechnung werden. Test — wenn ein Feature nur Sinn ergibt, um die Gegenseite bloßzustellen, fliegt es raus.

**Geklärt am 2026-08-24 (war blockierend):** Der Kaltstart ist rechtlich gangbar. IFG NRW greift, § 8 hat einen Public-Interest-Test, Aggregate umgehen § 9, Frist ein Monat, Ablehnung gebührenfrei. Gebührenrisiko 10–500 € je Auskunft — Minderung: erst kostenlose Landtags-Drucksachen ernten, dann nur Lücken anfragen. Details mit Quellen in §7 der Spec.

## Erledigt am 2026-08-24 (abends)

**~~1. Volle Datenlage-Recherche~~ — abgeschlossen.** Ein Durchlauf, Bericht: `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`. Umfang: 8.674 Dokumentnachweise, 159 PDFs (347 MB), 140 Antworten im Volltext geprüft. Werkzeuge und Rohdaten unter `research/`.

**~~2. Brückenkopf festlegen~~ — festgelegt: Heimatförderung NRW ("Starke Heimat Nordrhein-Westfalen"), Förderjahre 2018–2025.**

Die drei Befunde, die zählen:

- **Die Ader liegt in den Vorlagen, nicht in den Drucksachen.** Die Jahresberichte des Ministeriums an den Ausschuss für Heimat und Kommunales tragen die Tabellen — jedes Frühjahr neu, kostenlos, ohne Anfrage. Die Suche "Anfragen und Antworten" indexiert diese Klasse nicht; dafür braucht es die Parlamentsdatenbank.
- **Belegte Datenlage:** 3.317 Einzelanträge 2018–2019 mit Status und Ablehnungsgrund (Drs 17/9738); Anträge/bewilligt/abgelehnt je Förderelement 2021 (Vorl 17/6633); bewilligt/abgelehnt je Bezirksregierung 2024 (Vorl 18/3926); Einzelanträge mit Ablehnungsgrund 2023 und 2025 (Vorl 18/2806, 18/5027). Sechs von acht Förderjahren gedeckt; Lücken 2020 und 2022 → zwei gezielte IFG-Anfragen.
- **Die Konkurrenz fällt durch.** Von 140 geprüften Antwort-Drucksachen aus dem gesamten Förderumfeld enthalten 101 das Wort "abgelehnt" kein einziges Mal. EFRE-Empfängerlisten und NRW.BANK-Berichte führen ausschließlich Bewilligte.

## Was als Nächstes dran ist

**~~1. Abschnitt 3 des Designs~~ — erledigt am 2026-08-24.** Steht in der Spec als §12 (Prognose-Mechanik), §13 (Register-Datenmodell) und §14 (Teststrategie und Kill-Kriterium). Die vier Entscheidungen:

- **Prognose zweistufig gerechnet, einstufig angezeigt.** Erst Ausschlussprüfung gegen die belegten Ablehnungsgründe, dann Basisrate. Greift eine Regel, gibt es keine Prozentzahl, sondern den Grund samt Fundstelle. Die Ausschlussliste steht immer sichtbar, auch wenn alles bestanden ist.
- **Zwei Datenschichten.** Korpus (intern, je Entscheidung) und Register (veröffentlicht, aggregiert je §5.4). Jede Registerzahl trägt eine Herkunftsspalte: `gemessen`, `gezählt` oder `konflikt` — bei Konflikt werden beide Werte gezeigt, nie einer stillschweigend gewählt.
- **Klarnamen werden beim Import verworfen.** Nur der Antragstellertyp bleibt. Die Mehrfachantrags-Prüfung wandert dadurch in den Spiegel: gefragt statt nachgeschlagen.
- **Kill-Kriterium aus zwei Hürden.** Höchstens 1 % falsche „chancenlos"-Urteile *und* haltende Kalibrierungsintervalle. Bei Konflikt gewinnt die Absage-Hürde: lieber keine Zahl als eine falsche Abweisung.

**~~2. Implementierungsplan~~ — geschrieben am 2026-08-25:** `docs/superpowers/plans/2026-08-25-doorway-ernte-und-urteil.md`. 13 Tasks, 81 Schritte, vollständiger Code je Schritt.

Der Plan deckt bewusst nur **Teil 1** ab: Ernte, Korpus, Register, Prognose-Kern und das Kill-Kriterium — bis zu einem Kommandozeilenwerkzeug, das ausgibt, ob v1 live gehen darf. Grund für den Schnitt: Reißt Stufe 1 die 1-%-Hürde, darf die Oberfläche nie gebaut werden. Ein Plan, der beides umfasst, würde Arbeit einplanen, die von einem noch nicht gefällten Urteil abhängt. Spiegel, Weboberfläche und öffentliches Register bekommen einen eigenen Plan — danach.

**3. Ausführung** ← hier geht es weiter. Zwei Wege: `subagent-driven-development` (frischer Subagent je Task, Review dazwischen) oder `executing-plans` (in dieser Session, Checkpoints). Die Extraktionsskripte in `research/` bleiben Recherchewerkzeug; sie werden neu geschrieben, nicht übernommen.

## Offene Punkte, die eine Entscheidung von Felix brauchen

- ~~**Zeitbudget.**~~ Entschieden am 2026-08-25: Doorway ist Flaggschiff, `messen` und Nährboden geparkt (siehe oben).
- **Verhältnis zu `messen` und belegbar.eu.** Beide bleiben eigenständig, liefern aber Mechanik bzw. Disziplin. Ob eine gemeinsame Schicht entsteht, entscheidet sich erst, wenn beide sie brauchen — nicht jetzt.

## Wie eine neue Session hier einsteigt

1. `docs/superpowers/specs/2026-08-24-doorway-design.md` lesen — das ist die Wahrheit, diese Datei ist nur der Wegweiser.
2. `docs/recherche/2026-08-24-datenlage-landtag-nrw.md` lesen — dort steht, warum der Brückenkopf die Heimatförderung ist und welche Quellen belegt tragen bzw. belegt nicht tragen. Abschnitt 7 dort listet die Änderungen, die in die Spec eingearbeitet sind.
3. Der Brainstorming-Prozess ist abgeschlossen, der Plan geschrieben. Ab jetzt wird gebaut — aber ausschließlich entlang des Plans, Task für Task, jeder mit eigenem Testzyklus und eigenem Commit.
4. Direkt weitermachen mit Punkt 3 oben. Task 1 ist das Projektgerüst; Task 2 lädt die sechs Quelldokumente und friert sie per SHA-256 ein. Vor dem ersten Code den Plan lesen — er enthält den vollständigen Quelltext je Schritt, nicht nur Beschreibungen.
