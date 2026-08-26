# Doorway — Design (Abschnitt 1–3)

**Datum:** 2026-08-24
**Status:** Abschnitt 1, 2 und 3 abgestimmt. Plan geschrieben (`docs/superpowers/plans/2026-08-25-doorway-ernte-und-urteil.md`). Präambel ergänzt am 2026-08-25.
**Nicht mehr blockiert:** Die Rechtsfrage ist geklärt (§7), der Brückenkopf steht (§11). Grundlage dafür: `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`.

---

## Präambel — der Leitsatz (2026-08-25)

> **Wer hat wann was entschieden, mit welchem Grund, mit welcher Fundstelle — und lässt sich das von außen prüfen, ohne uns glauben zu müssen?**

Doorway ist nicht „Förderung finden“, sondern „Ablehnung nachprüfbar machen“. Jede Zahl, jede Prognose, jedes Feature in dieser Spec steht unter diesem Satz. Wo ein Abschnitt ihm widerspricht, gilt der Satz, und der Abschnitt wird geändert – datiert, nicht stillschweigend.

Der Grund liegt in der übergeordneten These (`~/THESE.md`): Vertrauen ohne Mechanismus ist Gewohnheit. Knapp ist nicht Intelligenz, sondern Haftung – dass eine Aussage über Zeit an jemanden gebunden bleibt. Die Verwaltung hat ihre Ablehnungsgründe bereits aufgeschrieben; Doorway bindet sie an Datum und Fundstelle und macht sie prüfbar. Das Nein-Register ist der Kern. Spiegel und Prognose sind Folgen davon, nicht umgekehrt.

Was das für diese Spec selbst heißt: Sie ist ein Beleg, kein Manifest. Jede Entscheidung trägt ihr Datum, damit sich später nachlesen lässt, was wir wann für richtig hielten und warum wir uns geirrt haben. Aus Geschichte lernt nur, wer sie festgehalten hat.

Prüffrage für jedes neue Feature: *Macht es eine Entscheidung nachprüfbarer – oder nur bequemer?* Nur-bequem wird nachrangig. Und weiterhin gilt §-Leitplanke: Doorway darf keine Abrechnung werden.

---

## 1. Herkunft

Ausgangspunkt war ein Podcast über Peter Thiel. Bewundert wurde nicht seine Politik, sondern sein Handwerk: kontrarianisches Denken, langfristige Positionierung, Netzwerke. Abgelehnt wurden seine Werte.

Aus der Analyse blieben zwei Korrekturen stehen, die dieses Projekt prägen:

1. **Der Motor ist das Geheimnis, nicht die Rhetorik.** Das Underdog-gegen-Eliten-Framing ist Wirkung, nicht Ursache. Der Kern ist: eine konkrete, unpopuläre, zutreffende Behauptung — plus ein winziger Markt, den man tatsächlich beherrschen kann. (PayPal: erst PalmPilot-Beaming, dann eBay-Powerseller. Die große Vision kam nachträglich.)
2. **"Klingt unmöglich" ist ein Symptom, kein Ziel.** Wer auf Unmöglichkeit zielt, bekommt Größenwahn. Wer auf ein präzises Geheimnis zielt, bekommt etwas, das dann unmöglich klingt.

## 2. Die These (das Geheimnis)

> **Stillstand ist kein Charakterproblem, sondern ein Auszahlungsproblem. Deutschland ist nicht faul geworden — es hat sich zwanzig Jahre lang Systeme gebaut, in denen Bewahren belohnt und Versuchen bestraft wird. Wer die Auszahlung ändert, ändert das Verhalten — ohne einen einzigen Menschen überzeugen zu müssen.**

Ergänzt um das Wie und das Wen:

> **Systeme, die Sicherheit maximieren, bauen Schwellen. Schwellen sortieren genau die aus, die es versuchen würden. Von außen sieht das aus wie Bequemlichkeit — und weil die Ausgesperrten unsichtbar bleiben, bestätigt sich der Eindruck selbst. Es ist keine Faulheit. Es ist Aussperrung, die sich als Faulheit tarnt.**

**Verworfene Vorstufe (bewusst dokumentiert):** "Leute sind zu faul." Das ist eine Charaktererklärung. Sie ist die Wertprämisse der Gegenseite, sie erklärt nichts und liefert keinen Bauplan. Sie führt zu Projekten, die Menschen ändern wollen — das skaliert nie. Die Systemerklärung führt zu Projekten, die Anreize ändern — dieselben Menschen verhalten sich dann anders, ohne überzeugt worden zu sein.

**Warum das die saubere Umkehrung von Thiel ist:** Seine Welt besteht aus Toren, durch die die Außergewöhnlichen gehen und dahinter abschöpfen. Diese These sagt: Die Tore sind das Problem, und hinter jedem steht jemand, der es versucht hätte. Niemand muss außergewöhnlich sein.

## 3. Name und Anspruch

- **Produkt:** Doorway — die Öffnung, also das, was bleibt, wenn die Tür weg ist.
- **Anspruch:** "Open the door of the future."
- **Deutsche Fassung am Brückenkopf:** "Wir machen die Tür auf — für die, die es versuchen wollen."
- **Datensatz:** Das Nein-Register.

Bewusst getrennt: Das Produkt bleibt sachlich, die Provokation sitzt im Artefakt, wo sie belegbar wahr ist statt Marketing. Englischer Name, deutscher Anspruch — der Preis dafür fällt am Brückenkopf an, der Nutzen im Endspiel.

## 4. Was Doorway ist

> **Doorway ist keine Maschine, die dich reinbringt. Es ist die Maschine, die dir vor der Tür die Wahrheit sagt.**

Kein Wettbewerber kann das kopieren — nicht aus technischen Gründen, sondern weil ihr Geschäftsmodell es verbietet. Ein Berater, der sagt "bewirb dich nicht", wird nicht bezahlt.

## 5. Die Maschine (v1)

1. **Der Spiegel** — Lagebeschreibung in normaler Sprache. Kein Formular, kein Fachvokabular. Wer die Begriffe nicht kennt, ist genau die Zielgruppe.
2. **Die Prognose** — "Deine Chance liegt bei etwa X %. Der Grund, an dem Leute wie du scheitern, ist Y." Mit ausgewiesener Unsicherheit, nie als Versprechen.
3. **Der Beleg** — jede Aussage über ein Programm mit Quelle, Datum und Prüfweg.
4. **Das Nein-Register** — öffentlich, durchsuchbar, kostenlos: **aggregiert je Programm und Jahr** — wie viele Anträge, wie viele Ablehnungen, welche Ablehnungsgründe in welcher Häufigkeit.

   **Wichtig, geklärt am 2026-08-24:** Das Register führt *keine Namen abgelehnter Antragsteller*. Erstens verbietet § 9 IFG NRW die Herausgabe personenbezogener Daten, während Aggregate gar nicht darunterfallen — die Statistik ist rechtlich der leichtere Weg, nicht der schwerere. Zweitens braucht die Prognose ohnehin Basisraten und Ablehnungsgrund-Verteilungen, keine Namen. Drittens verstieße das Anprangern Abgelehnter direkt gegen die Leitplanke in §10: Die Ausgesperrten bloßzustellen wäre das Gegenteil des Projektzwecks. Recht, Nutzen und Ethik zeigen hier in dieselbe Richtung.

## 6. Der Schnitt: was v1 ausdrücklich nicht tut

- **Kein Antragsschreiben.** Dort sitzt jeder Wettbewerber, dort liegt keine Asymmetrie, und ein KI-geschriebener Antrag, der durchfällt, verbrennt drei Monate echter Hoffnung von jemandem, der ohnehin ausgesperrt ist. Das wäre das Gegenteil der These.
- **Programmsuche ist nicht das Produkt.** Notwendig, aber die Förderdatenbank des Bundes ist kostenlos. Wer nur besser sucht, baut Software, keine Revolution.
- Kein Kontozwang, keine Beratung, kein Premium-Tarif, keine Bewertung von Behörden.

## 7. Kaltstart — und der offene Vorbehalt

Die Prognose braucht das Register. Das Register braucht Nutzer. Nutzer kommen wegen der Prognose. Daran sterben solche Projekte normalerweise.

**Ausweg: das Seed-Register wird aus öffentlichen Quellen gefüllt, bevor der erste Nutzer da ist.**

- Informationsfreiheitsgesetz NRW — Antrags- und Bewilligungszahlen, Ablehnungsgründe pro Programm/Jahr
- Kleine Anfragen im Landtag NRW — Abgeordnete fragen diese Zahlen routinemäßig ab, Antworten sind öffentliche Drucksachen
- Bei EU-kofinanzierten Programmen verpflichtend veröffentlichte Empfängerlisten
- fragdenstaat.de — bereits beantwortete Anfragen sparen Monate

### Rechtsprüfung — Stand 2026-08-24: bestanden

Die blockierende Frage ist beantwortet. Der Kaltstart ist rechtlich gangbar.

| Prüfpunkt | Befund | Quelle |
|---|---|---|
| Gibt es ein IFG in NRW? | Ja, IFG NRW. Voraussetzungslos, antragsgebunden. NRW hat **kein** Transparenzgesetz — es gibt nur eine laufende Initiative dafür. Also: aktiv anfragen, nicht auf Veröffentlichung warten. | ldi.nrw.de, transparenzranking.de |
| § 8 Betriebs- und Geschäftsgeheimnisse | Greift bei wirtschaftlichem Schaden — **aber NRW hat einen Public-Interest-Test**: Zugang trotzdem, wenn überwiegendes Allgemeininteresse besteht und der Schaden geringfügig wäre. Bei Aggregatstatistik ist beides erfüllbar. | fragdenstaat.de/gesetz/ifg-nrw |
| § 9 personenbezogene Daten | Blockiert Namen einzelner Antragsteller. Aggregate fallen nicht darunter. → bestimmt das Register-Design (siehe §5.4) | ebd. |
| § 6 laufende Verfahren | Blockiert nur Laufendes, nicht abgeschlossene Förderjahrgänge. → immer abgeschlossene Jahre anfragen | ebd. |
| § 7 Entscheidungsprozesse | Entwürfe und Vorbereitungen geschützt, **nach Verfahrensabschluss freizugeben** | ebd. |
| Frist | Unverzüglich, spätestens ein Monat (§ 5 Abs. 2) | ebd. |
| Kosten (§ 11 + VerwGebO IFG NRW) | Rahmengebühren: 10–500 € für umfangreiche schriftliche Auskunft, 10–1000 € bei außergewöhnlichem Aufwand mit Schwärzung. **Ablehnung ist gebührenfrei. Härtefallerlass auf Antrag möglich.** Einfache Auskünfte liegen am unteren Ende. | recht.nrw.de, fragdenstaat.de/recht |
| Praxisnachweis | Es existieren beantwortete FragDenStaat-Anfragen, die genau solche Programmzahlen geliefert haben (Beispiel: Förderprogramm Photovoltaik, 132 Anträge 2023) | fragdenstaat.de |

**Wichtigster strategischer Befund:** Die Gebühren sind das einzige echte Kostenrisiko, und es gibt eine **kostenlose Umgehung**: Antworten der Landesregierung auf **Kleine Anfragen im Landtag NRW** enthalten routinemäßig tabellarische Übersichten über gestellte, bewilligte und abgelehnte Anträge je Förderprogramm — als öffentliche Drucksache, frei abrufbar, über die Dokumentensuche des Landtags durchsuchbar. Beispiel gefunden: Förderprogramm "Heimat. Zukunft. Nordrhein-Westfalen" (rund 150 Mio. €, fünf Teilprogramme), mehrere Drucksachen der 17. und 18. Wahlperiode mit genau diesen Tabellen.

**Daraus folgt die Reihenfolge der Datenbeschaffung** (überarbeitet am 2026-08-24 nach der Datenlage-Recherche, siehe `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`):

1. **Zuerst die Vorlagen der Fachausschüsse ernten.** Ministerien berichten den Ausschüssen jährlich über ihre Förderprogramme; diese Berichte tragen die Antrags-, Bewilligungs- und Ablehnungstabellen. Kosten: null, Rhythmus: jährlich. **Wichtig: Die Landtags-Suche "Anfragen und Antworten" indexiert Vorlagen nicht** — dafür braucht es die Parlamentsdatenbank (`parlamentsdatenbank-suchergebnis.html`).
2. **Dann die Antwort-Drucksachen** auf Kleine und Große Anfragen. Sie liefern gelegentlich sehr reiche Anhänge (Drs 17/9738: 3.317 Einzelanträge mit Ablehnungsgrund), aber unzuverlässig — und seit 2024 verweisen sie überwiegend nur noch auf die Vorlagen weiter.
3. **Dann gezielt IFG-Anfragen** — nur für die Lücken, nur abgeschlossene Jahrgänge, nur Aggregate (billiger, weil keine Schwärzung nötig). Konkret offen: Heimatförderung 2020 und 2022.
4. **Pflichtveröffentlichungen bei EU-kofinanzierten Programmen: geprüft, für das Register untauglich.** Die EFRE/JTF-Liste der Vorhaben führt ausschließlich Bewilligte, ohne Statusspalte. Sie bleibt als Kontext- und Nennerquelle nützlich, füllt das Nein-Register aber nicht. Dasselbe gilt für die Europa-Scheck-"Zusagenliste" und die NRW.BANK-Berichte.
5. **Zuletzt Nutzermeldungen** mit Scoring Rule.

**Erzählung:** Das Tor wird nicht eingerissen. Es wird der Schlüssel benutzt, der öffentlich herumliegt und den niemand aufhebt.

## 8. Rollenteilung und Reihenfolge

Doorway verschmilzt drei Stränge. Jeder hat genau eine Aufgabe:

- **Körper** — die Domäne: Zugang zu öffentlichem Geld, der winzige Markt, der reale Underdog-Konflikt.
- **Herz** — die Proper Scoring Rule aus dem Projekt `messen`. Nicht Dekoration: Die zentrale Zusage ("ehrliche Prognose") ist eine Vorhersage; Vorhersagen brauchen Kalibrierung; Kalibrierung braucht Ground Truth von Nutzern; und Nutzer haben starke Anreize zu schönen (Ablehnungen sind peinlich, Bewilligungssummen werden aufgerundet). Die Scoring Rule ist die Standardlösung genau dafür. Auszahlung ohne Geld möglich: Wer ehrlich meldet, bekommt bessere Prognosen für den nächsten Antrag.
- **Gesetz** — die Belegbarkeits-Disziplin aus belegbar.eu. Jede Aussage belegt, datiert, nachprüfbar. Sonst ist Doorway nur ein weiteres undurchsichtiges Orakel, also genau das, wogegen es antritt.

**Reihenfolge — nicht verhandelbar, sonst stirbt es:**

1. These sofort verschmelzen: ein Name, eine Erzählung, ab Tag eins.
2. Das Gesetz ab Tag eins — als Disziplin, nicht als portierter Code. Kostet fast nichts.
3. ~~Das Herz erst einbauen, wenn der Datensatz groß genug ist, dass Kalibrierung Sinn ergibt.~~ **Korrigiert am 2026-08-24 durch den Befund in §12.3:** Nicht die Datenmenge macht Kalibrierung nötig, sondern die Wanderung der Basisrate selbst. Die Ablehnungsquote des Heimat-Schecks schwankt zwischen 24,4 % und 41,9 % — die Streuung zwischen den Förderjahren ist gut viermal so groß wie der Stichprobenfehler. Das Herz gehört deshalb **ab v1 hinein**, wenn auch in reduzierter Form: als gemessene Kalibrierung gegen die eigenen Backtests (§14), noch nicht als Anreizmechanik für Nutzermeldungen. Letztere kommt weiterhin erst, wenn Nutzer melden.
4. **Code niemals verschmelzen.** Was gebraucht wird, wird neu geschrieben. Wertvoll an `messen` ist die durchdachte Mechanik, nicht die Implementierung.

## 9. Wen Doorway ersetzt — ehrliche Abgrenzung

Die frühere Formulierung "eine ganze Beraterbranche wird überflüssig" war überzogen und wird hiermit korrigiert. Genauer:

| Wer | Ersetzt? |
|---|---|
| Fördermittel-Datenbanken im Abo | Ja, vollständig — reine Informationsrente |
| Freie Fördermittelberater im unteren/mittleren Segment (5–15 % Erfolgshonorar) | Ja, im Kern — das Wissen wird öffentlich |
| Spezialisten für komplexe EU-/Horizon-/ZIM-Anträge | Nein — dort ist echtes Handwerk |
| Wirtschaftsförderung, IHK, Verbände (kostenlos) | Nein, ergänzt sie |

Doorway ersetzt nicht das Schreiben. Es ersetzt das Torwächtern über Wissen.

**Der eigentliche Angriffspunkt ist das Erfolgshonorar.** Wer nur bei Bewilligung bezahlt wird, muss den Grenzfall ablehnen. Die Branche bedient damit strukturell die, die es ohnehin geschafft hätten, und weist die ab, die Hilfe am nötigsten hätten. Das ist die Schwelle in Reinform — entstanden aus einer Auszahlungsstruktur, nicht aus Bosheit. Angegriffen wird der Anreiz, nicht die Menschen.

## 10. Leitplanken

**Doorway darf keine Abrechnung werden.** Das Projekt entsteht aus einer persönlichen Verwundung (gescheiterter NRW-Antrag, nicht an der Idee, sondern an 21.000 Euro Vorfinanzierung). Das ist Treibstoff und macht zugleich blind.

**Konkreter Test:** Wenn ein Feature nur dann Sinn ergibt, wenn man die Gegenseite bloßstellen will, fliegt es raus. Nützlichkeit für den Ausgesperrten schlägt Schaden für den Torwächter, immer.

**Zweite Leitplanke:** Die Prognose verspricht nie Erfolg. Die gesamte Glaubwürdigkeit hängt daran, dass Doorway auch schlechte Nachrichten sagt. Der Name wurde bewusst so gewählt, dass er den Versuch verspricht und nicht das Ergebnis.

## 11. Offene Punkte und Risiken

| Punkt | Art | Stand |
|---|---|---|
| Fallen Förderstatistiken unter das IFG NRW? | ~~Blockierend~~ | **Geklärt 2026-08-24: ja, gangbar.** Siehe §7. Aggregate umgehen § 9, § 8 hat Public-Interest-Test, und Landtags-Drucksachen liefern einen Teil kostenlos. |
| Gebührenrisiko bei vielen IFG-Anfragen | Betrieb | 10–500 € je Auskunft möglich. Minderung: erst Drucksachen ernten, dann nur Lücken anfragen, nur Aggregate, Härtefallerlass beantragen. |
| Welche Programmfamilie hat die beste Datenlage? | ~~Blockierend für Brückenkopf~~ | **Geklärt 2026-08-24: Heimatförderung NRW ("Starke Heimat Nordrhein-Westfalen"), Förderjahre 2018–2025.** Sechs von acht Jahren mit Ablehnungszahlen belegt, vier davon mit Gründen auf Antragsebene; jährlicher Berichtsrhythmus. Von 140 volltextgeprüften Antworten aus dem übrigen Förderumfeld enthalten 101 das Wort "abgelehnt" nie. Bericht: `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`. |
| Prognose-Mechanik, Register-Datenmodell, Teststrategie | ~~Design~~ | **Geklärt 2026-08-24: §12, §13, §14.** Zweistufige Prognose (Regel vor Rate), Korpus/Register-Trennung mit Herkunftsspalte, Kill-Kriterium aus zwei Hürden mit Vorrang für die Absage. |
| Der Sammelgrund "entspricht nicht den Förderkriterien" | Datenqualität | 45,6 % aller Ablehnungen 2018–2019 tragen keine spezifische Begründung. Stufe 1 der Prognose kann diesen Block nicht auflösen; er fällt in die Basisrate. Grenze ist ausgewiesen (§12.1), nicht behoben. |
| Basisrate wandert mit der Verwaltungspraxis | Modell | Ablehnungsquote Heimat-Scheck schwankt 24,4 %–41,9 %. Behandelt in §12.3; zwingt das Herz aus §8 in v1 hinein. Bleibt beobachtungsbedürftig: Ein weiterer Sprung ändert die Intervallbreite. |
| Zeitbudget | Betrieb | ungelöst: rund 3 Stunden am Abend, vier laufende Projekte. Wird Doorway Flaggschiff, muss etwas anderes runter. Gehört entschieden, nicht vorgenommen. |
| Marktnähe zu vorhandenen Anbietern | Strategie | Der Unterschied muss die Transparenzschicht sein, nicht die Suche. Wird Doorway nur eine bessere Suche, ist die These verfehlt. |

**Brückenkopf-Entscheidung:** bewusst nach Datenlage statt nach Zielgruppen-Sympathie. Ein Register, das sich nicht füllen lässt, ist kein Projekt.

## 12. Die Prognose-Mechanik

**Grundsatz: zweistufig gerechnet, einstufig angezeigt.** Die Regelprüfung entscheidet, welche Zeile das Gewicht trägt — sie erzeugt keinen zweiten Bildschirm. Beide Fälle bekommen dasselbe Panel in derselben Anordnung, damit das Auge nach dem zweiten Mal weiß, wo es hinschauen muss.

### 12.1 Stufe 1 — die Ausschlussprüfung

Der Befund, der diese Stufe erzwingt: **Die Ablehnungen sind kategorisch, nicht graduell.** Wer Vereinstrikots beantragt, hat keine 38-%-Chance, sondern null. Eine Prognose, die Regelverletzer und echte Bewerber in eine Zahl mischt, ist im Einzelfall fast immer falsch, obwohl sie im Mittel stimmt.

Die belegten Ausschlussgründe (Quellen: Drs 17/9738 für 2018–2019, Vorl 18/5027 für 2025):

| Regel | Belegte Formulierungen in den Quellen |
|---|---|
| Antragsberechtigung | „fehlende Antragsberechtigung", z. B. Firmen |
| Vereinseigene Ausstattung | „Vereinsausstattung", „vereinsübliche Ausstattung", „vereinseigene Ausstattung", „Vereinsfahne", „Mobiliar", Uniformen, Trikots |
| Vereinsinterner Zweck | „vereinsintern", „übliche Vereinsarbeit"; auch reine Feiern, Speisen, Getränke, Ausflüge |
| Vorzeitiger Maßnahmenbeginn | „vorzeitiger Maßnahmenbeginn", „vorzeitiger Maßnahmebeginn" |
| Prüffähigkeit | „Antrag nicht prüffähig", fehlende plausible Kostenaufstellung trotz Nachfrage |
| Mehrfachantrag | mehr als ein Scheck pro Jahr und Antragstellendem (Förderrichtlinie) |

Greift eine Regel, lautet die Antwort nicht „X %", sondern: *„Das wird abgelehnt, und zwar aus diesem Grund — hier ist die Fundstelle."* Dazu, wo möglich, was stattdessen förderfähig wäre.

**Die Mehrfachantrags-Regel wird nicht nachgeschlagen, sondern gefragt.** Weil Klarnamen beim Import verworfen werden (§13.3), kann das Register nicht wissen, ob jemand dieses Jahr schon beantragt hat. Diese Prüfung gehört ohnehin in den Spiegel (§5.1) als Frage an den Nutzer — eine Sekunde Aufwand, und sie verlangt keine Datenbank über Vereine.

**Bekannte Grenze, die nicht kaschiert wird:** Von 1.219 Ablehnungen 2018–2019 tragen 556 — 45,6 % — nur die Begründung „entspricht nicht den Förderkriterien". Kein spezifischer Grund, nichts mechanisch Prüfbares. In den jüngeren Jahrgängen ist der Anteil dieses Sammelgrunds eher gestiegen. Stufe 1 kann nur die *benannten* Kategorien fangen; der größte Einzelblock bleibt undurchsichtig und fällt zwangsläufig in die Basisrate von Stufe 2. Doorway behauptet nicht, das aufzulösen — es weist aus, wie groß der undurchsichtige Rest ist.

### 12.2 Stufe 2 — die Basisrate

Greift keine Regel, kommt die Basisrate für *Förderelement × Förderjahr × Bewilligungsstelle*. Die Aufschlüsselung nach Förderelement ist der stärkste Prädiktor, den die Daten hergeben — stärker als jedes Nutzermerkmal:

| Förderelement | Ablehnungsquote 2018–2019 | 2025 |
|---|---|---|
| Heimat-Preis | 0,6 % | 0,0 % |
| Heimat-Fonds | 24,2 % | 25,0 % |
| Heimat-Zeugnis | 54,4 % | 31,6 % |
| Heimat-Werkstatt | 52,5 % | 36,0 % |
| Heimat-Scheck | 38,4 % | 35,6 % |

Die Bewilligungsstelle ist die zweite Dimension und keine Kosmetik: Im Förderjahr 2024 lehnte die Bezirksregierung Münster 22,5 % ab, Köln 39,4 % — gleiches Programm, gleiche Richtlinie, 1,75-facher Unterschied. Das Ministerium räumt die „uneinheitliche Bewilligungspraxis in den Bezirksregierungen" selbst ein (Vorl 18/3926).

### 12.3 Unsicherheit — der Befund, der alles andere bestimmt

Die Ablehnungsquote des Heimat-Schecks über die belegten Förderjahre:

| 2018 | 2019 | 2021 | 2024 | 2025 |
|---|---|---|---|---|
| 36,6 % | 39,8 % | **24,4 %** | **41,9 %** | 35,6 % |

Spannweite 17,4 Punkte. Dazwischen liegt keine Veränderung der Antragsteller, sondern eine Veränderung der Verwaltungspraxis — das Ministerium berichtet für 2025 ausdrücklich, nach „intensiven Gesprächen mit den Bezirksregierungen" sei die Zahl der Ablehnungen um 67 gefallen.

Daraus folgt die zentrale Regel für die Darstellung: **Die Unsicherheit wird von der Regimeschwankung bestimmt, nicht vom Stichprobenfehler.** Bei n = 926 beträgt der Stichprobenfehler ±3,1 Punkte (95 %), die Streuung zwischen den Förderjahren aber ±13,3 Punkte. Ein Intervall aus der Stichprobe wäre um den Faktor 4 zu selbstsicher. Ausgewiesen wird die größere der beiden Größen, nie die kleinere.

Das ist zugleich die These aus §2 auf der Zeitachse: Derselbe Antrag hatte 2021 eine 76-%-Chance und 2024 eine 58-%-Chance. Wer 2024 abgelehnt wurde, war nicht schlechter als der, der 2021 durchkam — er hat einen anderen Verwaltungszustand erwischt. Die Schwelle wandert, und niemand sagt es den Leuten.

### 12.4 Die Darstellung

Ein Panel, gleiche Anordnung in beiden Fällen. Von oben nach unten: Vorhaben und Einordnung; das Urteil (Regel oder Rate) als einzige hervorgehobene Zeile; die vollständige Ausschlussprüfung mit Häkchen; die Verteilung der Ablehnungsgründe für dieses Element und diese Stelle; die Belegzeile mit Dokument und Datum.

**Die Ausschlussprüfung steht immer da, auch wenn alles bestanden ist.** Das kostet vier Zeilen und liefert die Information, die sonst fehlt: nicht nur, *dass* die Chance bei 60 % liegt, sondern dass die bekannten Killer bereits ausgeschlossen sind. Wer nur eine Zahl sieht, weiß nicht, ob sie für ihn gilt.

---

## 13. Das Register-Datenmodell

Zwei Schichten, weil die Quellen zwei Granularitäten liefern. Manche Förderjahre kommen als Einzelentscheidungen (2018, 2019, 2023, 2025), andere nur als Aggregat (2021 je Förderelement, 2024 je Bezirksregierung). Ein Modell, das nur eine Form kennt, müsste die andere entweder wegwerfen oder erfinden.

### 13.1 Schicht 1 — der Korpus (intern, nicht veröffentlicht)

Eine Zeile je Entscheidung, so wie die Quelle sie hergibt, ohne Glättung:

```
programm · förderelement · förderjahr · kommune · bezirksregierung
antragstellertyp · vorhabenstext · betrag
antragsdatum · entscheidungsdatum
status (bewilligt | abgelehnt) · ablehnungsgrund_roh
quelle (dokument, seite) · extraktionslauf · geprüft_am
```

Der Korpus ist kein Nebenprodukt, sondern die Grundlage für Stufe 1 der Prognose. Ohne die Vorhabenstexte gibt es keine Regelerkennung.

**Ergänzt 2026-08-26:** Der Korpus liegt als `daten/korpus.jsonl` im Git-Repository, damit jede Änderung als Diff nachvollziehbar bleibt. Daraus folgt: Das Repository ist **privat**. Veröffentlicht wird ausschließlich das Register (§13.2). Die Git-Historie wurde am 26.08.2026 um ein Golden File mit einem Klarnamen aus der Antragsteller-Spalte der Drs 17/9738 bereinigt — die Quelle ist dort, anders als angenommen, nicht durchgehend anonymisiert; der Extraktor bildet die Spalte deshalb auf elf Typen ab, bevor irgendetwas gespeichert wird.

Felder, die eine Quelle nicht hergibt, bleiben leer. Sie werden nie geschätzt, interpoliert oder aus Nachbarjahren übernommen.

### 13.2 Schicht 2 — das Register (veröffentlicht, aggregiert je §5.4)

Eine Zeile je *Programm × Förderelement × Förderjahr × Bewilligungsstelle*:

```
anträge · bewilligt · abgelehnt · fördervolumen
ablehnungsgründe: verteilung
herkunft: gemessen | gezählt | konflikt
beleg: dokument, datum, seite, abrufdatum
```

**Die Herkunftsspalte ist nicht optional und wird nie leer.**

- `gemessen` — die Quelle nennt genau diese Zahl.
- `gezählt` — aus Einzelzeilen des Korpus aggregiert.
- `konflikt` — beides vorhanden und ungleich. Dann werden **beide Werte gespeichert und beide angezeigt**, nie stillschweigend einer gewählt oder gemittelt.

Der Konfliktfall ist kein Sonderfall, sondern Alltag. Vorl 18/5027 nennt im Fließtext 947 Bewilligungen und 329 Scheck-Ablehnungen; die eigene Anlage desselben Dokuments liefert 945 und 330. Für die Prognose sind ±2 aus 1.296 bedeutungslos. Für die Glaubwürdigkeit ist es alles: Wer Doorway prüfen will, nimmt den Bericht des Ministeriums und vergleicht. Steht dort 947 und bei uns 945 ohne Erklärung, sind wir ungenau. Steht bei uns „945 gezählt, 947 laut Bericht, Differenz dokumentiert", sind wir genauer als die Quelle — und das ist nachprüfbar. Das ist das Gesetz aus §8 in seiner konkretesten Form: **Nicht die Zahl ist der Beleg, sondern das Paar aus Zahl und Herkunft.**

### 13.3 Klarnamen werden beim Import verworfen

Die Quellen nennen Antragsteller mit Namen — Vereine, Stiftungen, Kommunen; natürliche Personen stehen bereits in der Quelle als „Privatperson". Doorway speichert diese Namen **gar nicht erst**. Erhalten bleibt nur der Antragstellertyp (Verein, Initiative, Vereinigung, Stiftung, Kommune, Privatperson, Firma).

Begründung: §5.4 sagt „niemals namentlich", §10 verbietet alles, was nur zum Bloßstellen taugt. Was nicht gespeichert ist, kann nicht lecken und nicht versehentlich veröffentlicht werden. Doorway kann so nicht einmal aus Versehen zur Liste der abgelehnten Schützenvereine werden.

Der Preis ist benannt: Eine Verifikation Zeile für Zeile gegen die Quelle ist nicht möglich. Dafür bleibt die Quelle selbst öffentlich verlinkt, mit Dokument, Seite und Abrufdatum — jeder kann dort nachsehen.

---

## 14. Teststrategie und Kill-Kriterium

### 14.1 Vier Ebenen

**1. Extraktionstests (Golden Files).** Die Quelldokumente ändern sich nie — ein PDF von 2020 bleibt ein PDF von 2020. Die Extraktion ist damit vollständig deterministisch und einfrierbar: `Vorl 18/5027 → 1.296 Zeilen, 945 bewilligt, 351 abgelehnt`. Jede Parser-Änderung, die das verschiebt, fällt sofort auf.

**2. Selbstwiderspruchs-Tests.** Jedes Dokument, das ein Aggregat nennt *und* eine Anlage hat, wird automatisch gegen sich selbst geprüft. Die Differenz +2/−1 aus Vorl 18/5027 wird zum erwarteten, dokumentierten Wert — nicht zur Überraschung.

**3. Kalibrierungs-Backtest.** Der eigentliche Test der Kernzusage, und er ist mit den vorhandenen Daten lauffähig: Basisraten aus den früheren Förderjahren bilden, spätere vorhersagen, Fehler messen. Das Kriterium ist nicht „der Fehler ist null", sondern **„die tatsächliche Quote liegt innerhalb des ausgewiesenen Intervalls"**. Eine Prognose darf falsch liegen; sie darf nicht überrascht sein.

**4. Leitplanken-Test als Code.** Ein Test, der die gesamte veröffentlichte Ausgabe gegen die Namen in den Quelldokumenten hält und fehlschlägt, sobald ein Vereinsname durchrutscht. Die Leitplanke aus §10 steht dann nicht in einem Dokument, sondern in der Testsuite.

### 14.2 Das Kill-Kriterium für v1

**Beide Hürden müssen grün sein, sonst geht v1 nicht live.**

| Hürde | Schwelle |
|---|---|
| Stufe 1 — falsche Absagen | Von allen Urteilen „chancenlos" dürfen im Backtest **höchstens 1 %** doch bewilligt worden sein. |
| Stufe 2 — Kalibrierung | Jede ausgewiesene Klasse muss im Backtest innerhalb ihres angegebenen Intervalls liegen. |

**Bei Konflikt gewinnt Stufe 1.** Lieber gar keine Prozentzahl anzeigen, als jemanden falsch abweisen. Begründung aus §6: Wer jemanden vom Antrag abhält, der gewonnen hätte, richtet genau den Schaden an, gegen den das Projekt antritt.

**Präzisiert 2026-08-26, nach dem vierten Urteil aus Teil 1:** Die Kalibrierung prüft nur Vorhersagen, denen **mindestens drei belegte Förderjahre** zugrunde liegen. Jahre mit weniger Vorgeschichte sind Lernjahre, keine Prüfjahre — und für Kombinationen mit weniger als drei belegten Jahren zeigt das Panel **keine Prozentzahl**, nur Register und Ausschlussprüfung. Grund: 2018 ist für alle Elemente das erste Jahr (keine Vergleichsschwankung für 2019), und der Einbruch 2019→2021 nach der Corona-Lücke ist aus zwei Jahren mit keinem ehrlichen Intervall vorhersehbar. Gemessen: Fonds 26→6 %, Scheck 40→24 %, Werkstatt 54→13 %, Zeugnis 55→17 %. Mit drei Jahren trifft die Prognose — alle fünf Elemente 2025 lagen im Intervall. Die Hürde wird damit nicht gelockert, sondern auf die Fälle beschränkt, in denen überhaupt eine Zahl ausgewiesen wird. Gibt es keine einzige prüfbare Vorhersage, gilt die Hürde als **nicht bestanden** — kein Freifahrtschein durch Datenmangel.

Bewusst **nicht** gemessen wird, wie viele Chancenlose Stufe 1 übersieht. Eine Warnung zu wenig ist verzeihlich, eine zu viel nicht. Ebenso wenig gemessen wird, wie *eng* die Intervalle aus Stufe 2 sind — weite Intervalle sind erlaubt, solange sie ehrlich sind. Der Name verspricht den Versuch, nicht das Ergebnis (§10).

---

## 15. Nächste Schritte

1. ~~Rechtsfrage IFG NRW klären (blockierend)~~ — erledigt 2026-08-24, siehe §7.
2. ~~Datenlage-Recherche~~ — erledigt 2026-08-24. Bericht: `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`.
3. ~~Brückenkopf festlegen~~ — **Heimatförderung NRW ("Starke Heimat Nordrhein-Westfalen"), Förderjahre 2018–2025.** Register-Granularität: Programm × Förderelement × Jahr × Bezirksregierung.
4. ~~Abschnitt 3 des Designs~~ — erledigt 2026-08-24: §12 Prognose-Mechanik, §13 Register-Datenmodell, §14 Teststrategie und Kill-Kriterium.
5. ~~Implementierungsplan~~ — geschrieben 2026-08-25: `docs/superpowers/plans/2026-08-25-doorway-ernte-und-urteil.md` (13 Tasks). Deckt Teil 1 ab: bis zum Urteil des Kill-Kriteriums. Teil 2 — Spiegel, Weboberfläche, öffentliches Register — bekommt einen eigenen Plan, und nur, wenn beide Hürden aus §14.2 halten.
6. ~~Ausführung Teil 1~~ — erledigt 2026-08-25/26 (`~/doorway`, `master`, 113 Tests). Vier Urteile gemessen, siehe `NAECHSTE-SCHRITTE.md`. Hürde 2 riss strukturell; §14.2 am 26.08. präzisiert.
7. **Kill-Kriterium unter der präzisierten Hürde messen** ← hier geht es weiter. Halten beide Hürden, wird Teil 2 geplant.

**Was Abschnitt 3 für den Implementierungsplan festlegt:**

- **Reihenfolge der Arbeit ergibt sich aus dem Kill-Kriterium.** Stufe 1 hat Vorrang vor Stufe 2 (§14.2), also wird die Ausschlussprüfung vor der Basisraten-Rechnung gebaut und geprüft. Ohne bestandene Stufe 1 ist eine Prozentzahl wertlos.
- **Die Extraktion ist der Flaschenhals, nicht die Prognose.** Die Tabellen aus Drs 17/9738 lesen sich sauber mit `find_tables()`; die Vorlagen-Tabellen haben keine Linien und brauchen koordinatenbasiertes Zeilen-Clustering. Prototypen liegen in `research/`, sind aber Recherchewerkzeug und keine Pipeline — sie werden neu geschrieben, nicht übernommen.
- **Der erste lauffähige Test ist der Golden File**, nicht der Prognose-Backtest: `Vorl 18/5027 → 1.296 Zeilen, 945 bewilligt, 351 abgelehnt`. Er kostet wenig und friert die Extraktion sofort ein.
- **Offen und weiterhin Felix' Entscheidung:** das Zeitbudget, und ob `messen` oder belegbar.eu in Doorway aufgehen (§11).
