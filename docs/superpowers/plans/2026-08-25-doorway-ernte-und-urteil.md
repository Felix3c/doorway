# Doorway v1, Teil 1: Ernte und Urteil — Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein Kommandozeilenwerkzeug, das aus den öffentlichen Landtagsdokumenten zur NRW-Heimatförderung ein belegtes Register aufbaut, daraus eine zweistufige Prognose stellt und ausgibt, ob das Kill-Kriterium aus §14.2 der Spec erfüllt ist.

**Architecture:** Eine Kette aus vier Schichten, jede für sich testbar. *Extraktion* liest die Quell-PDFs koordinatenbasiert in Zeilen; *Korpus* hält eine Zeile je Entscheidung, ohne Klarnamen; *Register* aggregiert und markiert jede Zahl mit ihrer Herkunft; *Prognose* prüft erst Ausschlussregeln, dann Basisraten. Der Backtest misst am Ende beide Hürden des Kill-Kriteriums. Kein Web, keine Datenbank, keine Oberfläche — die kommen in Teil 2, und nur, wenn das Kriterium hält.

**Tech Stack:** Python ≥ 3.11, `src/`-Layout, pytest (`pythonpath = ["src"]`), PyMuPDF für die PDF-Extraktion. Korpus als JSONL, Register als CSV und JSON — beide git-versioniert, damit jede Änderung als Diff sichtbar ist. Testnamen auf Deutsch, Funktions- und Variablennamen englisch, wie in `~/messen`.

**Spec:** `docs/superpowers/specs/2026-08-24-doorway-design.md` (Abschnitt 1–3 vollständig)

**Recherchegrundlage:** `docs/recherche/2026-08-24-datenlage-landtag-nrw.md`

## Global Constraints

- **Klarnamen werden nie gespeichert** (§13.3). Kein Feld im Korpus oder Register nimmt einen Antragstellernamen auf. Erhalten bleibt nur der Antragstellertyp: `Verein`, `Vereinigung`, `Initiative`, `Stiftung`, `Kirche`, `Verband`, `gGmbH`, `Kommune`, `Privatperson`, `Firma`, `unbekannt`.
- **Keine Zahl ohne Herkunft** (§13.2). Jede Registerzeile trägt `herkunft ∈ {"gemessen", "gezaehlt", "konflikt"}`. Bei `konflikt` werden beide Werte gespeichert und beide ausgegeben; nie wird einer stillschweigend gewählt oder gemittelt.
- **Fehlende Felder bleiben leer** (§13.1). Nie schätzen, interpolieren oder aus Nachbarjahren übernehmen. `None` in einer Registerdimension bedeutet „über alle", nicht „unbekannt".
- **Bei Konflikt gewinnt die Absage** (§14.2). Reißt eine Ausschlussregel die 1-%-Hürde, wird sie abgeschaltet oder enger gefasst — nicht die Hürde gelockert.
- **Die Unsicherheit wird von der Regimeschwankung bestimmt** (§12.3), nie vom Stichprobenfehler allein. Ausgewiesen wird immer die größere der beiden Größen.
- **Python ≥ 3.11**, Abhängigkeiten minimal: `pymupdf>=1.24` zur Laufzeit, `pytest>=8.0` in der Entwicklung. Nichts weiter ohne ausdrücklichen Grund.
- **Alle Quelldokumente sind unveränderlich.** Ein PDF von 2020 bleibt ein PDF von 2020. Extraktionsergebnisse werden deshalb als Golden Files eingefroren.

## File Structure

| Datei | Verantwortung |
|---|---|
| `pyproject.toml` | Projektdefinition, Abhängigkeiten, pytest-Konfiguration |
| `src/doorway/quellen.py` | Registry der Quelldokumente: ID, URL, Datum, Förderjahr, Art |
| `src/doorway/laden.py` | Herunterladen, lokal cachen, per SHA-256 gegen eine Lockdatei prüfen |
| `src/doorway/tabellen.py` | Wörter einer PDF-Seite nach Koordinaten zu Zeilen und Spalten gruppieren |
| `src/doorway/extraktion/anlage_2025.py` | Extraktor für die Einzelfall-Anlage in Vorl 18/5027 |
| `src/doorway/extraktion/drucksache_2020.py` | Extraktor für die Linien-Tabelle in Drs 17/9738 |
| `src/doorway/extraktion/aggregate.py` | Extraktoren für die Übersichten in Vorl 17/6633 und Vorl 18/3926 |
| `src/doorway/korpus.py` | Datentyp `Entscheidung`, Namensverwerfung, JSONL-Persistenz |
| `src/doorway/register.py` | Datentyp `Registerzeile`, Aggregation, Herkunft, Konflikterkennung |
| `src/doorway/genannt.py` | Selbstwiderspruchs-Test: genannte Aggregate gegen die eigene Zählung |
| `src/doorway/regeln.py` | Stufe 1: Ausschlussregeln und ihre gemessene Treffsicherheit |
| `src/doorway/basisrate.py` | Stufe 2: Punktschätzer und Intervall aus Regimeschwankung |
| `src/doorway/prognose.py` | Zusammenführung beider Stufen, Textpanel |
| `src/doorway/backtest.py` | Kalibrierungsprüfung und Kill-Kriterium-Bericht |
| `src/doorway/cli.py` | Einstiegspunkt: `laden`, `ernten`, `prognose`, `kill-kriterium` |
| `golden/` | Eingefrorene Extraktionsergebnisse als JSON, git-versioniert |
| `golden/genannte-aggregate.json` | Von den Berichten im Fließtext genannte Zahlen, je mit wörtlichem Zitat |
| `daten/quellen/` | Heruntergeladene PDFs, **nicht** git-versioniert |
| `daten/quellen.lock.json` | SHA-256 je Quelldokument, git-versioniert |
| `daten/korpus.jsonl` | Eine Zeile je Entscheidung, git-versioniert |
| `daten/register.csv`, `daten/register.json` | Erzeugtes Register, git-versioniert |

**Testabhängigkeiten:** Die Extraktionstests (Task 4–6) und der Zitat-Test in Task 9 brauchen die PDFs; sie überspringen sich selbst, wenn die Dateien fehlen. Alles Übrige ab Task 7 läuft gegen die eingefrorenen Golden Files und braucht kein Netz.

**Reihenfolge:** Task 1–8 bauen die Kette bis zum Register. Task 9 prüft sie gegen sich selbst. Task 10–13 sind die Prognose und ihr Urteil, in der Reihenfolge, die das Kill-Kriterium vorgibt: Stufe 1 vor Stufe 2, beide vor dem Backtest.

---

### Task 1: Projektgerüst und Quellenregister

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `src/doorway/__init__.py`
- Create: `src/doorway/quellen.py`
- Test: `tests/test_quellen.py`

**Interfaces:**
- Consumes: nichts
- Produces: `Quelle` (frozen dataclass: `id: str`, `dokument: str`, `datum: date`, `foerderjahre: tuple[int, ...]`, `art: Literal["einzelfaelle","aggregat","nur_ablehnungen"]`, `seiten: int`, `beschreibung: str`; Properties `url: str`, `dateiname: str`), `QUELLEN: dict[str, Quelle]`, `quelle(id: str) -> Quelle`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_quellen.py
from datetime import date

import pytest

from doorway.quellen import QUELLEN, quelle


def test_registry_enthaelt_die_sechs_belegten_dokumente():
    assert set(QUELLEN) == {
        "drs-17-9738",
        "vorl-17-2268",
        "vorl-17-6633",
        "vorl-18-2806",
        "vorl-18-3926",
        "vorl-18-5027",
    }


def test_jede_quelle_zeigt_auf_das_landtagsarchiv():
    for q in QUELLEN.values():
        assert q.url.startswith(
            "https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/"
        )
        assert q.url.endswith(".pdf")


def test_jedes_belegte_foerderjahr_hat_mindestens_eine_quelle():
    abgedeckt = {j for q in QUELLEN.values() for j in q.foerderjahre}
    assert {2018, 2019, 2021, 2023, 2024, 2025} <= abgedeckt


def test_die_luecken_2020_und_2022_sind_nicht_abgedeckt():
    abgedeckt = {j for q in QUELLEN.values() for j in q.foerderjahre}
    assert 2020 not in abgedeckt
    assert 2022 not in abgedeckt


def test_quelle_liefert_das_dokument_zum_bezeichner():
    q = quelle("vorl-18-5027")
    assert q.dokument == "MMV18-5027"
    assert q.datum == date(2026, 4, 21)
    assert q.foerderjahre == (2025,)
    assert q.art == "einzelfaelle"
    assert q.dateiname == "MMV18-5027.pdf"


def test_quelle_wirft_bei_unbekanntem_bezeichner():
    with pytest.raises(KeyError):
        quelle("gibt-es-nicht")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_quellen.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway'`

- [ ] **Step 3: Write the project scaffolding**

```toml
# pyproject.toml
[project]
name = "doorway"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pymupdf>=1.24"]

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
doorway = "doorway.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

```
# .gitignore
daten/quellen/
__pycache__/
*.egg-info/
.pytest_cache/
```

```python
# src/doorway/__init__.py
"""Doorway — sagt vor der Tür die Wahrheit."""
```

- [ ] **Step 4: Write the source registry**

```python
# src/doorway/quellen.py
"""Register der Quelldokumente.

Alle Dokumente sind öffentliche Drucksachen und Vorlagen des Landtags
Nordrhein-Westfalen und unveränderlich. Belege siehe
docs/recherche/2026-08-24-datenlage-landtag-nrw.md.
"""

from dataclasses import dataclass
from datetime import date
from typing import Literal

ARCHIV = "https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/"

Art = Literal["einzelfaelle", "aggregat", "nur_ablehnungen"]


@dataclass(frozen=True)
class Quelle:
    id: str
    dokument: str
    datum: date
    foerderjahre: tuple[int, ...]
    art: Art
    seiten: int
    beschreibung: str

    @property
    def url(self) -> str:
        return f"{ARCHIV}{self.dokument}.pdf"

    @property
    def dateiname(self) -> str:
        return f"{self.dokument}.pdf"


_ALLE = [
    Quelle(
        id="drs-17-9738",
        dokument="MMD17-9738",
        datum=date(2020, 6, 12),
        foerderjahre=(2018, 2019),
        art="einzelfaelle",
        seiten=139,
        beschreibung="Antwort auf Kleine Anfrage 3655; Anlage mit allen Anträgen "
        "2018-2019, Status und Ablehnungsgrund",
    ),
    Quelle(
        id="vorl-17-2268",
        dokument="MMV17-2268",
        datum=date(2019, 7, 5),
        foerderjahre=(2018,),
        art="nur_ablehnungen",
        seiten=94,
        beschreibung="Übersicht der abgelehnten Anträge der Heimatförderung für 2018",
    ),
    Quelle(
        id="vorl-17-6633",
        dokument="MMV17-6633",
        datum=date(2022, 3, 22),
        foerderjahre=(2021,),
        art="aggregat",
        seiten=56,
        beschreibung="Übersicht Heimatförderung 2021: Anträge, bewilligt, abgelehnt "
        "und Fördervolumen je Förderelement",
    ),
    Quelle(
        id="vorl-18-2806",
        dokument="MMV18-2806",
        datum=date(2024, 7, 19),
        foerderjahre=(2023,),
        art="nur_ablehnungen",
        seiten=112,
        beschreibung="Anlage 3: Abgelehnte Anträge Förderjahr 2023 mit Ablehnungsgrund",
    ),
    Quelle(
        id="vorl-18-3926",
        dokument="MMV18-3926",
        datum=date(2025, 5, 23),
        foerderjahre=(2024,),
        art="aggregat",
        seiten=47,
        beschreibung="Förderjahr 2024: bewilligte und abgelehnte Anträge je "
        "Bezirksregierung",
    ),
    Quelle(
        id="vorl-18-5027",
        dokument="MMV18-5027",
        datum=date(2026, 4, 21),
        foerderjahre=(2025,),
        art="einzelfaelle",
        seiten=39,
        beschreibung="Förderjahr 2025: Anlage mit allen Entscheidungen, Bewilligung "
        "oder Ablehnung samt Grund",
    ),
]

QUELLEN: dict[str, Quelle] = {q.id: q for q in _ALLE}


def quelle(id: str) -> Quelle:
    """Liefert die Quelle zum Bezeichner. Wirft KeyError, wenn es sie nicht gibt."""
    return QUELLEN[id]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_quellen.py -v`
Expected: PASS, 6 Tests

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore src/doorway/__init__.py src/doorway/quellen.py tests/test_quellen.py
git commit -m "feat: Projektgeruest und Register der sechs belegten Quelldokumente"
```

---

### Task 2: Quelldokumente laden und per Prüfsumme einfrieren

**Files:**
- Create: `src/doorway/laden.py`
- Create: `daten/quellen.lock.json` (im Schritt erzeugt)
- Test: `tests/test_laden.py`

**Interfaces:**
- Consumes: `doorway.quellen.Quelle`, `doorway.quellen.QUELLEN`
- Produces: `pfad(q: Quelle, verzeichnis: Path) -> Path`, `pruefsumme(datei: Path) -> str`, `laden(q: Quelle, verzeichnis: Path, hole: Callable[[str], bytes] = ...) -> Path`, `lock_schreiben(verzeichnis: Path, lockdatei: Path) -> dict[str, str]`, `lock_pruefen(verzeichnis: Path, lockdatei: Path) -> list[str]`

Der Netzzugriff kommt als Parameter `hole` herein. Dadurch braucht kein Test das Netz.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_laden.py
import hashlib

import pytest

from doorway.laden import laden, lock_pruefen, lock_schreiben, pfad, pruefsumme
from doorway.quellen import quelle

Q = quelle("vorl-18-5027")


def test_pruefsumme_ist_sha256_des_inhalts(tmp_path):
    datei = tmp_path / "x.pdf"
    datei.write_bytes(b"%PDF-1.7 test")
    assert pruefsumme(datei) == hashlib.sha256(b"%PDF-1.7 test").hexdigest()


def test_laden_holt_die_datei_nur_einmal(tmp_path):
    aufrufe = []

    def hole(url):
        aufrufe.append(url)
        return b"%PDF-1.7 inhalt"

    laden(Q, tmp_path, hole=hole)
    laden(Q, tmp_path, hole=hole)
    assert aufrufe == [Q.url]
    assert pfad(Q, tmp_path).read_bytes() == b"%PDF-1.7 inhalt"


def test_laden_lehnt_ab_was_kein_pdf_ist(tmp_path):
    with pytest.raises(ValueError, match="kein PDF"):
        laden(Q, tmp_path, hole=lambda url: b"<html>Fehlerseite</html>")


def test_lock_schreiben_und_pruefen_findet_keine_abweichung(tmp_path):
    laden(Q, tmp_path, hole=lambda url: b"%PDF-1.7 inhalt")
    lock = tmp_path / "quellen.lock.json"
    eintraege = lock_schreiben(tmp_path, lock)
    assert eintraege[Q.id] == pruefsumme(pfad(Q, tmp_path))
    assert lock_pruefen(tmp_path, lock) == []


def test_lock_pruefen_meldet_eine_veraenderte_datei(tmp_path):
    laden(Q, tmp_path, hole=lambda url: b"%PDF-1.7 inhalt")
    lock = tmp_path / "quellen.lock.json"
    lock_schreiben(tmp_path, lock)
    pfad(Q, tmp_path).write_bytes(b"%PDF-1.7 etwas anderes")
    assert lock_pruefen(tmp_path, lock) == [Q.id]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_laden.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.laden'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/laden.py
"""Quelldokumente holen, lokal ablegen und gegen eine Lockdatei prüfen.

Die Dokumente sind unveränderlich. Ändert sich eine Prüfsumme, hat sich
entweder das Archiv geändert oder die lokale Datei ist beschädigt — in
beiden Fällen darf nicht stillschweigend weitergerechnet werden.
"""

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Callable

from .quellen import QUELLEN, Quelle

BLOCK = 1 << 20


def _hole_ueber_netz(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as antwort:
        return antwort.read()


def pfad(q: Quelle, verzeichnis: Path) -> Path:
    return Path(verzeichnis) / q.dateiname


def pruefsumme(datei: Path) -> str:
    h = hashlib.sha256()
    with open(datei, "rb") as f:
        while stueck := f.read(BLOCK):
            h.update(stueck)
    return h.hexdigest()


def laden(
    q: Quelle,
    verzeichnis: Path,
    hole: Callable[[str], bytes] = _hole_ueber_netz,
) -> Path:
    """Lädt das Dokument, falls es lokal noch nicht liegt. Gibt den Pfad zurück."""
    ziel = pfad(q, verzeichnis)
    if ziel.exists() and ziel.stat().st_size > 0:
        return ziel
    inhalt = hole(q.url)
    if not inhalt.startswith(b"%PDF"):
        raise ValueError(f"{q.id}: Antwort ist kein PDF ({inhalt[:40]!r})")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(inhalt)
    return ziel


def lock_schreiben(verzeichnis: Path, lockdatei: Path) -> dict[str, str]:
    """Schreibt die Prüfsummen aller lokal vorhandenen Quellen."""
    eintraege = {
        q.id: pruefsumme(pfad(q, verzeichnis))
        for q in QUELLEN.values()
        if pfad(q, verzeichnis).exists()
    }
    Path(lockdatei).parent.mkdir(parents=True, exist_ok=True)
    Path(lockdatei).write_text(
        json.dumps(eintraege, indent=1, sort_keys=True), encoding="utf-8"
    )
    return eintraege


def lock_pruefen(verzeichnis: Path, lockdatei: Path) -> list[str]:
    """Gibt die Bezeichner der Quellen zurück, deren Prüfsumme abweicht."""
    erwartet = json.loads(Path(lockdatei).read_text(encoding="utf-8"))
    abweichend = []
    for id, summe in erwartet.items():
        datei = pfad(QUELLEN[id], verzeichnis)
        if not datei.exists() or pruefsumme(datei) != summe:
            abweichend.append(id)
    return sorted(abweichend)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_laden.py -v`
Expected: PASS, 5 Tests

- [ ] **Step 5: Fetch the real documents and write the lockfile**

```bash
python -c "
from pathlib import Path
from doorway.laden import laden, lock_schreiben
from doorway.quellen import QUELLEN
ziel = Path('daten/quellen')
for q in QUELLEN.values():
    print(q.id, laden(q, ziel))
print(len(lock_schreiben(ziel, Path('daten/quellen.lock.json'))), 'Pruefsummen')
"
```

Expected: Sechs Dateien in `daten/quellen/`, Ausgabe `6 Pruefsummen`.

- [ ] **Step 6: Commit**

```bash
git add src/doorway/laden.py tests/test_laden.py daten/quellen.lock.json
git commit -m "feat: Quelldokumente laden und per SHA-256 einfrieren"
```

---

### Task 3: Wörter einer PDF-Seite zu Zeilen und Spalten gruppieren

**Files:**
- Create: `src/doorway/tabellen.py`
- Test: `tests/test_tabellen.py`

**Interfaces:**
- Consumes: nichts (reine Funktionen über Wortlisten)
- Produces: `Wort` (NamedTuple `x: float`, `y: float`, `text: str`), `woerter_der_seite(seite) -> list[Wort]`, `zeilen(woerter: Iterable[Wort], toleranz: float = 2.0) -> list[list[Wort]]`, `spalte(zeile: Iterable[Wort], von: float, bis: float) -> str`

Die Vorlagen-Tabellen haben keine Linien; ein linienbasierter Tabellenfinder sieht sie nicht. Die Wortpositionen verraten sie zuverlässig.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_tabellen.py
from doorway.tabellen import Wort, spalte, zeilen


def test_woerter_gleicher_hoehe_bilden_eine_zeile():
    w = [
        Wort(63, 100.0, "Attendorn"),
        Wort(179, 100.4, "Heimat-Preis"),
        Wort(840, 101.0, "5.000,00"),
    ]
    assert [[x.text for x in z] for z in zeilen(w)] == [
        ["Attendorn", "Heimat-Preis", "5.000,00"]
    ]


def test_zeilen_werden_nach_hoehe_sortiert_ausgegeben():
    w = [Wort(63, 200.0, "unten"), Wort(63, 100.0, "oben")]
    assert [z[0].text for z in zeilen(w)] == ["oben", "unten"]


def test_woerter_einer_zeile_werden_nach_x_sortiert():
    w = [Wort(840, 100.0, "rechts"), Wort(63, 100.0, "links")]
    assert [x.text for x in zeilen(w)[0]] == ["links", "rechts"]


def test_zu_weit_auseinander_liegende_hoehen_sind_zwei_zeilen():
    w = [Wort(63, 100.0, "eins"), Wort(63, 112.0, "zwei")]
    assert len(zeilen(w)) == 2


def test_spalte_fasst_die_woerter_eines_x_bereichs_zusammen():
    z = [
        Wort(63, 100.0, "Bad"),
        Wort(78, 100.0, "Berleburg"),
        Wort(179, 100.0, "Heimat-Scheck"),
    ]
    assert spalte(z, 50, 170) == "Bad Berleburg"
    assert spalte(z, 170, 260) == "Heimat-Scheck"


def test_spalte_ist_leer_wenn_der_bereich_kein_wort_enthaelt():
    z = [Wort(63, 100.0, "Bad")]
    assert spalte(z, 800, 900) == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_tabellen.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.tabellen'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/tabellen.py
"""Wörter einer PDF-Seite nach Koordinaten zu Zeilen und Spalten gruppieren.

Die Ausschussvorlagen enthalten Tabellen ohne Linien. Ein linienbasierter
Tabellenfinder sieht sie nicht; die Wortpositionen verraten sie zuverlässig.
"""

from typing import Iterable, NamedTuple


class Wort(NamedTuple):
    x: float
    y: float
    text: str


def woerter_der_seite(seite) -> list[Wort]:
    """Wandelt die Wortliste einer PyMuPDF-Seite in Wort-Tupel."""
    return [Wort(w[0], w[1], w[4]) for w in seite.get_text("words")]


def zeilen(woerter: Iterable[Wort], toleranz: float = 2.0) -> list[list[Wort]]:
    """Bündelt Wörter zu Zeilen.

    Zwei Wörter gehören zusammen, wenn ihre Oberkanten weniger als
    `toleranz` auseinanderliegen.
    """
    sortiert = sorted(woerter, key=lambda w: (w.y, w.x))
    gebuendelt: list[list[Wort]] = []
    for w in sortiert:
        if gebuendelt and abs(w.y - gebuendelt[-1][0].y) <= toleranz:
            gebuendelt[-1].append(w)
        else:
            gebuendelt.append([w])
    return [sorted(z, key=lambda w: w.x) for z in gebuendelt]


def spalte(zeile: Iterable[Wort], von: float, bis: float) -> str:
    """Fügt die Wörter zusammen, deren x-Position in [von, bis) liegt."""
    return " ".join(w.text for w in zeile if von <= w.x < bis).strip()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_tabellen.py -v`
Expected: PASS, 6 Tests

- [ ] **Step 5: Commit**

```bash
git add src/doorway/tabellen.py tests/test_tabellen.py
git commit -m "feat: koordinatenbasiertes Zeilen- und Spalten-Clustering fuer linienlose Tabellen"
```

---

### Task 4: Extraktor für die Einzelfall-Anlage 2025 und ihr Golden File

**Files:**
- Create: `src/doorway/extraktion/__init__.py`
- Create: `src/doorway/extraktion/anlage_2025.py`
- Create: `golden/vorl-18-5027.json` (im Schritt erzeugt)
- Test: `tests/test_extraktion_anlage_2025.py`

**Interfaces:**
- Consumes: `doorway.tabellen.woerter_der_seite`, `doorway.tabellen.zeilen`, `doorway.tabellen.spalte`
- Produces: `SPALTEN: dict[str, tuple[float, float]]`, `ELEMENTE: set[str]`, `anlagenseiten(dok) -> list[int]`, `extrahieren(pdf: Path) -> list[dict]` — jedes dict mit den Schlüsseln `kommune`, `foerderelement`, `vorhabentext`, `betrag_euro`, `status`, `ablehnungsgrund_roh`, `seite`

Die Spaltengrenzen sind an den gemessenen Wortpositionen des Dokuments abgelesen: Kommune ab x=50, Förderbereich ab 170, Vorhaben ab 260, Fördernehmende ab 570, Betrag ab 830, Status ab 870, Ablehnungsgrund ab 950. Die Spalte `Fördernehmende` wird gelesen, aber nicht übernommen (Global Constraint: keine Klarnamen).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_extraktion_anlage_2025.py
import json
from pathlib import Path

import pytest

from doorway.extraktion.anlage_2025 import extrahieren
from doorway.laden import pfad
from doorway.quellen import quelle

PDF = pfad(quelle("vorl-18-5027"), Path("daten/quellen"))
GOLDEN = Path("golden/vorl-18-5027.json")

pytestmark = pytest.mark.skipif(
    not PDF.exists(), reason="Quelldokument fehlt — erst `doorway laden` ausfuehren"
)


@pytest.fixture(scope="module")
def gelesen():
    return extrahieren(PDF)


def test_die_anlage_enthaelt_1296_entscheidungen(gelesen):
    assert len(gelesen) == 1296


def test_945_bewilligungen_und_351_ablehnungen(gelesen):
    assert sum(1 for z in gelesen if z["status"] == "bewilligt") == 945
    assert sum(1 for z in gelesen if z["status"] == "abgelehnt") == 351


def test_jede_zeile_traegt_genau_einen_der_beiden_status(gelesen):
    assert {z["status"] for z in gelesen} == {"bewilligt", "abgelehnt"}


def test_die_foerderelemente_sind_die_fuenf_bekannten(gelesen):
    assert {z["foerderelement"] for z in gelesen} == {
        "Heimat-Scheck",
        "Heimat-Preis",
        "Heimat-Fonds",
        "Heimat-Werkstatt",
        "Heimat-Zeugnis",
    }


def test_der_heimat_scheck_hat_596_bewilligungen_und_330_ablehnungen(gelesen):
    scheck = [z for z in gelesen if z["foerderelement"] == "Heimat-Scheck"]
    assert sum(1 for z in scheck if z["status"] == "bewilligt") == 596
    assert sum(1 for z in scheck if z["status"] == "abgelehnt") == 330


def test_der_heimat_preis_wurde_kein_einziges_mal_abgelehnt(gelesen):
    preis = [z for z in gelesen if z["foerderelement"] == "Heimat-Preis"]
    assert sum(1 for z in preis if z["status"] == "abgelehnt") == 0


def test_kein_feld_traegt_einen_antragstellernamen(gelesen):
    assert all("foerdernehmende" not in z for z in gelesen)
    assert all("e.V." not in (z["vorhabentext"] or "") for z in gelesen)


def test_ein_vorhaben_mit_dem_wort_webseite_ueberlebt_den_kopfzeilenfilter(gelesen):
    """Der Filter darf nur den Zeilenanfang pruefen.

    Eine Pruefung auf "Seite" als Teilstring wuerde "Neugestaltung der
    Webseite" verschlucken und die Gesamtzahl still verfaelschen.
    """
    assert any("ebseite" in (z["vorhabentext"] or "") for z in gelesen)


def test_das_ergebnis_stimmt_mit_dem_golden_file_ueberein(gelesen):
    assert gelesen == json.loads(GOLDEN.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_extraktion_anlage_2025.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.extraktion'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/extraktion/__init__.py
"""Extraktoren, je einer pro Quelldokument.

Jedes Dokument hat sein eigenes Layout. Sechs spezielle Extraktoren sind
genauer als ein allgemeiner und lassen sich einzeln einfrieren.
"""
```

```python
# src/doorway/extraktion/anlage_2025.py
"""Vorl 18/5027, Anlage: alle Entscheidungen des Förderjahres 2025.

Spalten laut Kopfzeile: Kommune, Förderbereich, Kurzbezeichnung des Vorhabens,
Fördernehmende, Bewilligung (in Euro, gerundet), Ablehnung, Ablehnungsgrund.

Die Spalte "Fördernehmende" wird bewusst nicht übernommen (§13.3 der Spec).
"""

import re
from decimal import Decimal
from pathlib import Path

import pymupdf

from ..tabellen import spalte, woerter_der_seite, zeilen

SPALTEN = {
    "kommune": (50.0, 170.0),
    "foerderelement": (170.0, 260.0),
    "vorhabentext": (260.0, 570.0),
    "_foerdernehmende": (570.0, 830.0),
    "betrag": (830.0, 870.0),
    "status": (870.0, 950.0),
    "ablehnungsgrund_roh": (950.0, 2000.0),
}

ELEMENTE = {
    "Heimat-Scheck",
    "Heimat-Preis",
    "Heimat-Fonds",
    "Heimat-Werkstatt",
    "Heimat-Zeugnis",
}

# Kopf- und Fusszeilen werden am ersten Wort erkannt, nicht per Teilstring:
# ein Vorhaben heisst "Neugestaltung der Webseite", und eine Pruefung auf
# "Seite" im ganzen Text wuerde diese Datenzeile stillschweigend verschlucken.
ZEILENANFANG = ("Seite", "Ministerium", "Bau", "des", "Kommune", "Ablehnungsgrund")


def anlagenseiten(dok) -> list[int]:
    """Seitenindizes, auf denen die Anlagen-Kopfzeile steht."""
    return [i for i in range(dok.page_count) if "Ablehnungsgrund" in dok[i].get_text()]


def _betrag(text: str) -> str | None:
    treffer = re.search(r"\d{1,3}(?:\.\d{3})*,\d{2}", text or "")
    if not treffer:
        return None
    roh = treffer.group(0).replace(".", "").replace(",", ".")
    return str(Decimal(roh))


def extrahieren(pdf: Path) -> list[dict]:
    """Liest alle Entscheidungszeilen der Anlage."""
    dok = pymupdf.open(pdf)
    ergebnis: list[dict] = []
    for seite in anlagenseiten(dok):
        for zeile in zeilen(woerter_der_seite(dok[seite])):
            if not zeile or zeile[0].text in ZEILENANFANG:
                continue
            element = spalte(zeile, *SPALTEN["foerderelement"])
            if element not in ELEMENTE:
                continue
            grund = spalte(zeile, *SPALTEN["ablehnungsgrund_roh"])
            marke = spalte(zeile, *SPALTEN["status"]).lower()
            if grund or marke.startswith("abgelehnt"):
                status = "abgelehnt"
            elif marke.startswith("bewilligt"):
                status = "bewilligt"
            else:
                continue
            ergebnis.append(
                {
                    "kommune": spalte(zeile, *SPALTEN["kommune"]) or None,
                    "foerderelement": element,
                    "vorhabentext": spalte(zeile, *SPALTEN["vorhabentext"]) or None,
                    "betrag_euro": _betrag(spalte(zeile, *SPALTEN["betrag"])),
                    "status": status,
                    "ablehnungsgrund_roh": grund or None,
                    "seite": seite + 1,
                }
            )
    return ergebnis
```

- [ ] **Step 4: Run the counting tests before freezing**

Run: `python -m pytest tests/test_extraktion_anlage_2025.py -v -k "not golden"`
Expected: Die acht Zähl- und Leitplankentests bestehen; nur `test_das_ergebnis_stimmt_mit_dem_golden_file_ueberein` schlägt fehl, weil die Datei noch nicht existiert.

Weicht eine Zahl ab, ist der Extraktor falsch, **nicht** der Test. Die Zahlen sind in `docs/recherche/2026-08-24-datenlage-landtag-nrw.md` belegt.

- [ ] **Step 5: Freeze the golden file**

```bash
python -c "
import json
from pathlib import Path
from doorway.extraktion.anlage_2025 import extrahieren
Path('golden').mkdir(exist_ok=True)
gelesen = extrahieren(Path('daten/quellen/MMV18-5027.pdf'))
Path('golden/vorl-18-5027.json').write_text(
    json.dumps(gelesen, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(gelesen), 'Zeilen eingefroren')
"
```

Expected: `1296 Zeilen eingefroren`

- [ ] **Step 6: Run the full test to verify it passes**

Run: `python -m pytest tests/test_extraktion_anlage_2025.py -v`
Expected: PASS, 9 Tests

- [ ] **Step 7: Commit**

```bash
git add src/doorway/extraktion/ tests/test_extraktion_anlage_2025.py golden/vorl-18-5027.json
git commit -m "feat: Extraktor fuer die Einzelfall-Anlage 2025, Golden File eingefroren"
```

---

### Task 5: Extraktor für die Linien-Tabelle 2018/2019 und ihr Golden File

**Files:**
- Create: `src/doorway/extraktion/drucksache_2020.py`
- Create: `golden/drs-17-9738.json` (im Schritt erzeugt)
- Test: `tests/test_extraktion_drucksache_2020.py`

**Interfaces:**
- Consumes: nichts aus `tabellen` — dieses Dokument hat echte Tabellenlinien und wird mit PyMuPDFs `find_tables()` gelesen
- Produces: `SPALTEN: list[str]`, `LANGFORM: dict[str, str]`, `extrahieren(pdf: Path) -> list[dict]` mit den Schlüsseln `bezirksregierung`, `kommune`, `foerderelement`, `antragstellertyp`, `vorhabentext`, `betrag_euro`, `antragsdatum`, `entscheidungsdatum`, `status`, `ablehnungsgrund_roh`, `seite`

Die Anlage hat elf Spalten in fester Reihenfolge. Die Förderelemente stehen hier ohne Präfix (`Scheck` statt `Heimat-Scheck`) und werden beim Einlesen auf die lange Form normalisiert. Datumsangaben werden als ISO-Datum (`2018-08-22`) ausgegeben, damit sich das Förderjahr später ohne Neuformatierung ablesen lässt.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_extraktion_drucksache_2020.py
import json
from pathlib import Path

import pytest

from doorway.extraktion.drucksache_2020 import extrahieren
from doorway.laden import pfad
from doorway.quellen import quelle

PDF = pfad(quelle("drs-17-9738"), Path("daten/quellen"))
GOLDEN = Path("golden/drs-17-9738.json")

pytestmark = pytest.mark.skipif(
    not PDF.exists(), reason="Quelldokument fehlt — erst `doorway laden` ausfuehren"
)


@pytest.fixture(scope="module")
def gelesen():
    return extrahieren(PDF)


def test_die_anlage_enthaelt_3317_entscheidungen(gelesen):
    assert len(gelesen) == 3317


def test_2098_bewilligungen_und_1219_ablehnungen(gelesen):
    assert sum(1 for z in gelesen if z["status"] == "bewilligt") == 2098
    assert sum(1 for z in gelesen if z["status"] == "abgelehnt") == 1219


def test_antragsjahr_2018_hat_912_bewilligungen_und_508_ablehnungen(gelesen):
    j = [z for z in gelesen if (z["antragsdatum"] or "").startswith("2018")]
    assert sum(1 for z in j if z["status"] == "bewilligt") == 912
    assert sum(1 for z in j if z["status"] == "abgelehnt") == 508


def test_antragsjahr_2019_hat_1185_bewilligungen_und_708_ablehnungen(gelesen):
    j = [z for z in gelesen if (z["antragsdatum"] or "").startswith("2019")]
    assert sum(1 for z in j if z["status"] == "bewilligt") == 1185
    assert sum(1 for z in j if z["status"] == "abgelehnt") == 708


def test_die_foerderelemente_werden_auf_die_lange_form_normalisiert(gelesen):
    elemente = {z["foerderelement"] for z in gelesen}
    assert "Heimat-Scheck" in elemente
    assert "Scheck" not in elemente


def test_haeufigster_ablehnungsgrund_ist_der_sammelgrund(gelesen):
    gruende = [z["ablehnungsgrund_roh"] for z in gelesen if z["status"] == "abgelehnt"]
    assert sum(1 for g in gruende if g == "entspricht nicht den Förderkriterien") == 556


def test_die_fuenf_regierungsbezirke_kommen_alle_vor(gelesen):
    assert {"Arnsberg", "Detmold", "Düsseldorf", "Köln", "Münster"} <= {
        z["bezirksregierung"] for z in gelesen
    }


def test_das_ergebnis_stimmt_mit_dem_golden_file_ueberein(gelesen):
    assert gelesen == json.loads(GOLDEN.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_extraktion_drucksache_2020.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.extraktion.drucksache_2020'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/extraktion/drucksache_2020.py
"""Drs 17/9738, Anlage: alle Anträge der Heimatförderung 2018 und 2019.

Diese Anlage hat echte Tabellenlinien; PyMuPDFs find_tables() liest sie
sauber in elf Spalten. Klarnamen enthält sie nicht — die Landesregierung
hat die Antragstellenden bereits selbst anonymisiert.
"""

import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pymupdf

SPALTEN = [
    "_lfd",
    "bezirksregierung",
    "kommune",
    "foerderelement",
    "antragstellertyp",
    "vorhabentext",
    "betrag_euro",
    "antragsdatum",
    "entscheidungsdatum",
    "status",
    "ablehnungsgrund_roh",
]

LANGFORM = {
    "Scheck": "Heimat-Scheck",
    "Preis": "Heimat-Preis",
    "Fonds": "Heimat-Fonds",
    "Werkstatt": "Heimat-Werkstatt",
    "Zeugnis": "Heimat-Zeugnis",
}


def _datum(text: str) -> str | None:
    treffer = re.search(r"\d{2}\.\d{2}\.\d{4}", text or "")
    if not treffer:
        return None
    return datetime.strptime(treffer.group(0), "%d.%m.%Y").date().isoformat()


def _betrag(text: str) -> str | None:
    treffer = re.search(r"\d{1,3}(?:\.\d{3})*,\d{2}", text or "")
    if not treffer:
        return None
    return str(Decimal(treffer.group(0).replace(".", "").replace(",", ".")))


def extrahieren(pdf: Path) -> list[dict]:
    """Liest alle Antragszeilen der Anlage."""
    dok = pymupdf.open(pdf)
    ergebnis: list[dict] = []
    for nr in range(dok.page_count):
        for tabelle in dok[nr].find_tables().tables:
            for roh in tabelle.extract():
                zellen = [re.sub(r"\s+", " ", (c or "")).strip() for c in roh]
                if len(zellen) < len(SPALTEN):
                    continue
                feld = dict(zip(SPALTEN, zellen))
                status = feld["status"].lower()
                if status not in ("bewilligt", "abgelehnt"):
                    continue
                element = LANGFORM.get(feld["foerderelement"])
                if element is None:
                    continue
                ergebnis.append(
                    {
                        "bezirksregierung": feld["bezirksregierung"] or None,
                        "kommune": feld["kommune"] or None,
                        "foerderelement": element,
                        "antragstellertyp": feld["antragstellertyp"] or None,
                        "vorhabentext": feld["vorhabentext"] or None,
                        "betrag_euro": _betrag(feld["betrag_euro"]),
                        "antragsdatum": _datum(feld["antragsdatum"]),
                        "entscheidungsdatum": _datum(feld["entscheidungsdatum"]),
                        "status": status,
                        "ablehnungsgrund_roh": feld["ablehnungsgrund_roh"] or None,
                        "seite": nr + 1,
                    }
                )
    return ergebnis
```

- [ ] **Step 4: Run the counting tests before freezing**

Run: `python -m pytest tests/test_extraktion_drucksache_2020.py -v -k "not golden"`
Expected: Die sieben Zähltests bestehen; nur der Golden-Test schlägt fehl.

Hinweis zur erwarteten Zeilenzahl: In der Rohtabelle steht in einer Zeile der Ortsname `Overath` in der Förderelement-Spalte — ein Fehler der Quelle. Die Normalisierung über `LANGFORM` verwirft diese Zeile. Das ist beabsichtigt: lieber eine Zeile weniger als eine erfundene.

- [ ] **Step 5: Freeze the golden file**

```bash
python -c "
import json
from pathlib import Path
from doorway.extraktion.drucksache_2020 import extrahieren
gelesen = extrahieren(Path('daten/quellen/MMD17-9738.pdf'))
Path('golden/drs-17-9738.json').write_text(
    json.dumps(gelesen, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(gelesen), 'Zeilen eingefroren')
"
```

Expected: `3317 Zeilen eingefroren`

- [ ] **Step 6: Run the full test to verify it passes**

Run: `python -m pytest tests/test_extraktion_drucksache_2020.py -v`
Expected: PASS, 8 Tests

- [ ] **Step 7: Commit**

```bash
git add src/doorway/extraktion/drucksache_2020.py tests/test_extraktion_drucksache_2020.py golden/drs-17-9738.json
git commit -m "feat: Extraktor fuer die Anlage 2018/2019, Golden File eingefroren"
```

---

### Task 6: Extraktoren für die beiden Aggregatquellen

**Files:**
- Create: `src/doorway/extraktion/aggregate.py`
- Create: `golden/vorl-17-6633.json`, `golden/vorl-18-3926.json` (im Schritt erzeugt)
- Test: `tests/test_extraktion_aggregate.py`

**Interfaces:**
- Consumes: `doorway.tabellen.woerter_der_seite`, `doorway.tabellen.zeilen`
- Produces: `uebersicht_2021(pdf: Path) -> list[dict]` mit `foerderelement`, `antraege`, `bewilligt`, `abgelehnt`, `foerdervolumen_euro`, `seite`; `uebersicht_2024(pdf: Path) -> list[dict]` mit `bewilligungsstelle`, `bewilligt`, `foerdervolumen_euro`, `abgelehnt`, `seite`

Diese beiden Quellen liefern **keine Einzelfälle**, sondern fertige Aggregate — jeweils nur auf einer Achse. Vorl 17/6633 gliedert 2021 nach Förderelement ohne Bezirksregierung, Vorl 18/3926 gliedert 2024 nach Bezirksregierung ohne Förderelement. Beide füllen den Registerschlüssel nur zur Hälfte; die jeweils andere Dimension bleibt `None` und bedeutet „über alle". In beiden Übersichten ist die letzte Zeile die Summenzeile; sie trägt `None` in der Achsenspalte.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_extraktion_aggregate.py
import json
from pathlib import Path

import pytest

from doorway.extraktion.aggregate import uebersicht_2021, uebersicht_2024
from doorway.laden import pfad
from doorway.quellen import quelle

PDF_2021 = pfad(quelle("vorl-17-6633"), Path("daten/quellen"))
PDF_2024 = pfad(quelle("vorl-18-3926"), Path("daten/quellen"))

pytestmark = pytest.mark.skipif(
    not (PDF_2021.exists() and PDF_2024.exists()),
    reason="Quelldokumente fehlen — erst `doorway laden` ausfuehren",
)


def test_uebersicht_2021_liefert_fuenf_elemente_und_die_summenzeile():
    assert [z["foerderelement"] for z in uebersicht_2021(PDF_2021)] == [
        "Heimat-Scheck",
        "Heimat-Preis",
        "Heimat-Fonds",
        "Heimat-Werkstatt",
        "Heimat-Zeugnis",
        None,
    ]


def test_uebersicht_2021_liest_den_heimat_scheck_korrekt():
    scheck = uebersicht_2021(PDF_2021)[0]
    assert (scheck["antraege"], scheck["bewilligt"], scheck["abgelehnt"]) == (
        1125,
        850,
        275,
    )
    assert scheck["foerdervolumen_euro"] == "1700000.00"


def test_uebersicht_2021_summenzeile_stimmt_mit_der_summe_der_elemente():
    zeilen = uebersicht_2021(PDF_2021)
    elemente, gesamt = zeilen[:-1], zeilen[-1]
    assert gesamt["antraege"] == sum(z["antraege"] for z in elemente) == 1513
    assert gesamt["bewilligt"] == sum(z["bewilligt"] for z in elemente) == 1219
    assert gesamt["abgelehnt"] == sum(z["abgelehnt"] for z in elemente) == 294


def test_uebersicht_2024_liefert_fuenf_bezirksregierungen_und_die_summenzeile():
    assert [z["bewilligungsstelle"] for z in uebersicht_2024(PDF_2024)] == [
        "Arnsberg",
        "Detmold",
        "Düsseldorf",
        "Köln",
        "Münster",
        None,
    ]


def test_uebersicht_2024_liest_koeln_und_muenster_korrekt():
    nach_stelle = {z["bewilligungsstelle"]: z for z in uebersicht_2024(PDF_2024)}
    assert (nach_stelle["Köln"]["bewilligt"], nach_stelle["Köln"]["abgelehnt"]) == (134, 87)
    assert (nach_stelle["Münster"]["bewilligt"], nach_stelle["Münster"]["abgelehnt"]) == (124, 36)


def test_uebersicht_2024_summenzeile_ist_883_bewilligt_und_427_abgelehnt():
    gesamt = uebersicht_2024(PDF_2024)[-1]
    assert gesamt["bewilligt"] == 883
    assert gesamt["abgelehnt"] == 427


def test_beide_uebersichten_stimmen_mit_ihren_golden_files_ueberein():
    assert uebersicht_2021(PDF_2021) == json.loads(
        Path("golden/vorl-17-6633.json").read_text(encoding="utf-8")
    )
    assert uebersicht_2024(PDF_2024) == json.loads(
        Path("golden/vorl-18-3926.json").read_text(encoding="utf-8")
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_extraktion_aggregate.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.extraktion.aggregate'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/extraktion/aggregate.py
"""Die beiden Quellen, die fertige Aggregate liefern statt Einzelfälle.

Vorl 17/6633 gliedert das Förderjahr 2021 nach Förderelement, ohne
Bezirksregierung. Vorl 18/3926 gliedert das Förderjahr 2024 nach
Bezirksregierung, ohne Förderelement. Beide füllen den Registerschlüssel
nur zur Hälfte; die fehlende Dimension bleibt None und heißt "über alle".
"""

import re
from decimal import Decimal
from pathlib import Path

import pymupdf

from ..tabellen import woerter_der_seite, zeilen

ELEMENTE_2021 = {
    "Scheck": "Heimat-Scheck",
    "Preis": "Heimat-Preis",
    "Fonds": "Heimat-Fonds",
    "Werkstatt": "Heimat-Werkstatt",
    "Zeugnis": "Heimat-Zeugnis",
}

BEZIRKE = ("Arnsberg", "Detmold", "Düsseldorf", "Köln", "Münster")


def _zahl(text: str) -> int:
    return int(text.replace(".", ""))


def _euro_aus_betrag(text: str) -> str:
    return str(Decimal(text.replace(".", "").replace(",", ".")).quantize(Decimal("0.01")))


def _euro_aus_ganzzahl(text: str) -> str:
    return str(Decimal(text.replace(".", "")).quantize(Decimal("0.01")))


def _seite_mit(dok, marker: str) -> int:
    for i in range(dok.page_count):
        if marker in dok[i].get_text():
            return i
    raise LookupError(f"Marker {marker!r} nicht gefunden")


def uebersicht_2021(pdf: Path) -> list[dict]:
    """Liest die Tabelle 'Übersicht Heimatförderung 2021'."""
    dok = pymupdf.open(pdf)
    nr = _seite_mit(dok, "Übersicht Heimatförderung 2021")
    ergebnis: list[dict] = []
    for zeile in zeilen(woerter_der_seite(dok[nr])):
        woerter = [w.text for w in zeile]
        if not woerter:
            continue
        kopf = woerter[0]
        if kopf not in ELEMENTE_2021 and kopf != "Gesamt":
            continue
        zahlen = [w for w in woerter[1:] if re.fullmatch(r"[\d\.]+", w)]
        betraege = [w for w in woerter[1:] if re.fullmatch(r"[\d\.]+,\d{2}", w)]
        if len(zahlen) < 3 or not betraege:
            continue
        ergebnis.append(
            {
                "foerderelement": ELEMENTE_2021.get(kopf),
                "antraege": _zahl(zahlen[0]),
                "bewilligt": _zahl(zahlen[1]),
                "abgelehnt": _zahl(zahlen[2]),
                "foerdervolumen_euro": _euro_aus_betrag(betraege[-1]),
                "seite": nr + 1,
            }
        )
    return ergebnis


def uebersicht_2024(pdf: Path) -> list[dict]:
    """Liest 'Bewilligte Anträge 2024 nach Bezirksregierungen'."""
    dok = pymupdf.open(pdf)
    nr = _seite_mit(dok, "Bewilligte Anträge 2024 nach Bezirksregierungen")
    ergebnis: list[dict] = []
    for zeile in zeilen(woerter_der_seite(dok[nr])):
        woerter = [w.text for w in zeile]
        zahlen = [w for w in woerter if re.fullmatch(r"[\d\.]+", w)]
        if len(zahlen) != 3:
            continue
        stelle = woerter[0] if woerter[0] in BEZIRKE else None
        ergebnis.append(
            {
                "bewilligungsstelle": stelle,
                "bewilligt": _zahl(zahlen[0]),
                "foerdervolumen_euro": _euro_aus_ganzzahl(zahlen[1]),
                "abgelehnt": _zahl(zahlen[2]),
                "seite": nr + 1,
            }
        )
    return ergebnis
```

- [ ] **Step 4: Run the counting tests before freezing**

Run: `python -m pytest tests/test_extraktion_aggregate.py -v -k "not golden"`
Expected: Die sechs Zähltests bestehen; nur der Golden-Test schlägt fehl.

- [ ] **Step 5: Freeze both golden files**

```bash
python -c "
import json
from pathlib import Path
from doorway.extraktion.aggregate import uebersicht_2021, uebersicht_2024
for name, gelesen in [
    ('vorl-17-6633', uebersicht_2021(Path('daten/quellen/MMV17-6633.pdf'))),
    ('vorl-18-3926', uebersicht_2024(Path('daten/quellen/MMV18-3926.pdf'))),
]:
    Path(f'golden/{name}.json').write_text(
        json.dumps(gelesen, ensure_ascii=False, indent=1), encoding='utf-8')
    print(name, len(gelesen), 'Zeilen')
"
```

Expected: `vorl-17-6633 6 Zeilen` und `vorl-18-3926 6 Zeilen`

- [ ] **Step 6: Run the full test to verify it passes**

Run: `python -m pytest tests/test_extraktion_aggregate.py -v`
Expected: PASS, 7 Tests

- [ ] **Step 7: Commit**

```bash
git add src/doorway/extraktion/aggregate.py tests/test_extraktion_aggregate.py golden/vorl-17-6633.json golden/vorl-18-3926.json
git commit -m "feat: Extraktoren fuer die Aggregatuebersichten 2021 und 2024"
```

---

### Task 7: Der Korpus — eine Zeile je Entscheidung, ohne Klarnamen

**Files:**
- Create: `src/doorway/korpus.py`
- Test: `tests/test_korpus.py`
- Test: `tests/test_leitplanke.py`

**Interfaces:**
- Consumes: die Golden Files aus Task 4 und 5
- Produces: `PROGRAMM: str`, `TYPEN: frozenset[str]`, `NAMENSMUSTER: re.Pattern`, `Entscheidung` (frozen dataclass mit den Feldern `programm, foerderelement, foerderjahr, kommune, bezirksregierung, antragstellertyp, vorhabentext, betrag_euro, antragsdatum, entscheidungsdatum, status, ablehnungsgrund_roh, quelle_id, quelle_seite` und der Methode `sortierschluessel()`), `aus_anlage_2025(zeilen) -> list[Entscheidung]`, `aus_drucksache_2020(zeilen) -> list[Entscheidung]`, `schreiben(entscheidungen, pfad) -> int`, `lesen(pfad) -> list[Entscheidung]`

`Entscheidung` hat **kein** Feld für den Antragstellernamen. Der Leitplanken-Test ist die codegewordene Fassung von §10 der Spec.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_korpus.py
from dataclasses import fields

import pytest

from doorway.korpus import Entscheidung, aus_anlage_2025, lesen, schreiben

ROH_2025 = [
    {
        "kommune": "Bad Berleburg",
        "foerderelement": "Heimat-Scheck",
        "vorhabentext": "Restaurierung Schuetzenfahne",
        "betrag_euro": "2000.00",
        "status": "abgelehnt",
        "ablehnungsgrund_roh": "vereinseigene Ausstattung",
        "seite": 21,
    },
    {
        "kommune": "Ahlen",
        "foerderelement": "Heimat-Scheck",
        "vorhabentext": "Backhaus",
        "betrag_euro": "5000.00",
        "status": "bewilligt",
        "ablehnungsgrund_roh": None,
        "seite": 16,
    },
]


def test_entscheidung_hat_kein_feld_fuer_den_antragstellernamen():
    namen = {f.name for f in fields(Entscheidung)}
    assert not namen & {"antragsteller", "foerdernehmende", "name", "verein"}


def test_aus_anlage_2025_setzt_programm_und_foerderjahr():
    e = aus_anlage_2025(ROH_2025)[0]
    assert e.programm == "Starke Heimat Nordrhein-Westfalen"
    assert e.foerderjahr == 2025
    assert e.quelle_id == "vorl-18-5027"


def test_aus_anlage_2025_uebernimmt_status_und_grund():
    abgelehnt, bewilligt = aus_anlage_2025(ROH_2025)
    assert abgelehnt.status == "abgelehnt"
    assert abgelehnt.ablehnungsgrund_roh == "vereinseigene Ausstattung"
    assert bewilligt.status == "bewilligt"
    assert bewilligt.ablehnungsgrund_roh is None


def test_aus_anlage_2025_laesst_unbekannte_felder_leer():
    e = aus_anlage_2025(ROH_2025)[0]
    assert e.bezirksregierung is None
    assert e.antragsdatum is None
    assert e.antragstellertyp is None


def test_schreiben_und_lesen_ergibt_dieselben_entscheidungen(tmp_path):
    entscheidungen = aus_anlage_2025(ROH_2025)
    datei = tmp_path / "korpus.jsonl"
    assert schreiben(entscheidungen, datei) == 2
    assert lesen(datei) == sorted(entscheidungen, key=Entscheidung.sortierschluessel)


def test_schreiben_sortiert_stabil_damit_diffs_lesbar_bleiben(tmp_path):
    datei = tmp_path / "korpus.jsonl"
    schreiben(aus_anlage_2025(ROH_2025), datei)
    erste = datei.read_text(encoding="utf-8")
    schreiben(aus_anlage_2025(list(reversed(ROH_2025))), datei)
    assert datei.read_text(encoding="utf-8") == erste


def test_ein_unbekannter_status_wird_abgelehnt():
    with pytest.raises(ValueError, match="Status"):
        aus_anlage_2025([{**ROH_2025[0], "status": "zurueckgezogen"}])
```

```python
# tests/test_leitplanke.py
"""§10 der Spec als Test: Doorway darf keine Abrechnung werden.

Was nicht gespeichert ist, kann nicht blossstellen. Dieser Test schlaegt
fehl, sobald ein Antragstellername in den Korpus geraet.
"""

import json
from pathlib import Path

import pytest

from doorway.korpus import NAMENSMUSTER, lesen

KORPUS = Path("daten/korpus.jsonl")


def test_das_namensmuster_erkennt_die_ueblichen_rechtsformen():
    assert NAMENSMUSTER.search("Schuetzenbruderschaft St. Josef e.V. 1593")
    assert NAMENSMUSTER.search("Buergerstiftung Ahaus gGmbH")
    assert NAMENSMUSTER.search("Heimatverein Dolberg e. V.")


def test_das_namensmuster_schlaegt_bei_normalen_vorhabentexten_nicht_an():
    assert not NAMENSMUSTER.search("Restaurierung Schuetzenfahne")
    assert not NAMENSMUSTER.search("Anschaffung einer Projektionsanlage")
    assert not NAMENSMUSTER.search("Digitalisierung des Ortsarchivs")


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_im_geernteten_korpus_steht_kein_antragstellername():
    treffer = [
        (e.quelle_id, e.vorhabentext)
        for e in lesen(KORPUS)
        if e.vorhabentext and NAMENSMUSTER.search(e.vorhabentext)
    ]
    assert treffer == [], f"Klarnamen im Korpus: {treffer[:5]}"


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_keine_zeile_des_korpus_traegt_ein_unerwartetes_feld():
    erlaubt = {
        "programm",
        "foerderelement",
        "foerderjahr",
        "kommune",
        "bezirksregierung",
        "antragstellertyp",
        "vorhabentext",
        "betrag_euro",
        "antragsdatum",
        "entscheidungsdatum",
        "status",
        "ablehnungsgrund_roh",
        "quelle_id",
        "quelle_seite",
    }
    for zeile in KORPUS.read_text(encoding="utf-8").splitlines():
        assert set(json.loads(zeile)) == erlaubt
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_korpus.py tests/test_leitplanke.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.korpus'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/korpus.py
"""Der Korpus: eine Zeile je Entscheidung, so wie die Quelle sie hergibt.

Nicht veröffentlicht (§13.1 der Spec). Enthält keine Antragstellernamen —
sie werden beim Import verworfen, nicht maskiert (§13.3).
"""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal

PROGRAMM = "Starke Heimat Nordrhein-Westfalen"

TYPEN = frozenset(
    {
        "Verein",
        "Vereinigung",
        "Initiative",
        "Stiftung",
        "Kirche",
        "Verband",
        "gGmbH",
        "Kommune",
        "Privatperson",
        "Firma",
        "unbekannt",
    }
)

NAMENSMUSTER = re.compile(
    r"\be\.\s?V\.|\bgGmbH\b|\bGmbH\b|\bStiftung\b|bruderschaft\b|verein\b",
    re.IGNORECASE,
)

Status = Literal["bewilligt", "abgelehnt"]


@dataclass(frozen=True)
class Entscheidung:
    programm: str
    foerderelement: str
    foerderjahr: int
    kommune: str | None
    bezirksregierung: str | None
    antragstellertyp: str | None
    vorhabentext: str | None
    betrag_euro: str | None
    antragsdatum: str | None
    entscheidungsdatum: str | None
    status: Status
    ablehnungsgrund_roh: str | None
    quelle_id: str
    quelle_seite: int

    def sortierschluessel(self) -> tuple:
        return (
            self.foerderjahr,
            self.foerderelement,
            self.bezirksregierung or "",
            self.kommune or "",
            self.vorhabentext or "",
            self.quelle_seite,
        )


def _status(roh: str) -> Status:
    if roh not in ("bewilligt", "abgelehnt"):
        raise ValueError(f"Unbekannter Status: {roh!r}")
    return roh


def aus_anlage_2025(zeilen: Iterable[dict]) -> list[Entscheidung]:
    """Wandelt die Rohzeilen aus Vorl 18/5027 in Entscheidungen."""
    return [
        Entscheidung(
            programm=PROGRAMM,
            foerderelement=z["foerderelement"],
            foerderjahr=2025,
            kommune=z.get("kommune"),
            bezirksregierung=None,
            antragstellertyp=None,
            vorhabentext=z.get("vorhabentext"),
            betrag_euro=z.get("betrag_euro"),
            antragsdatum=None,
            entscheidungsdatum=None,
            status=_status(z["status"]),
            ablehnungsgrund_roh=z.get("ablehnungsgrund_roh"),
            quelle_id="vorl-18-5027",
            quelle_seite=z["seite"],
        )
        for z in zeilen
    ]


def aus_drucksache_2020(zeilen: Iterable[dict]) -> list[Entscheidung]:
    """Wandelt die Rohzeilen aus Drs 17/9738 in Entscheidungen.

    Das Förderjahr ergibt sich aus dem Antragsdatum; fehlt es, wird die
    Zeile verworfen, statt ein Jahr zu raten.
    """
    ergebnis = []
    for z in zeilen:
        antrag = z.get("antragsdatum")
        if not antrag:
            continue
        typ = z.get("antragstellertyp")
        ergebnis.append(
            Entscheidung(
                programm=PROGRAMM,
                foerderelement=z["foerderelement"],
                foerderjahr=int(antrag[:4]),
                kommune=z.get("kommune"),
                bezirksregierung=z.get("bezirksregierung"),
                antragstellertyp=typ if typ in TYPEN else "unbekannt",
                vorhabentext=z.get("vorhabentext"),
                betrag_euro=z.get("betrag_euro"),
                antragsdatum=antrag,
                entscheidungsdatum=z.get("entscheidungsdatum"),
                status=_status(z["status"]),
                ablehnungsgrund_roh=z.get("ablehnungsgrund_roh"),
                quelle_id="drs-17-9738",
                quelle_seite=z["seite"],
            )
        )
    return ergebnis


def schreiben(entscheidungen: Iterable[Entscheidung], pfad: Path) -> int:
    """Schreibt den Korpus als JSONL, stabil sortiert."""
    sortiert = sorted(entscheidungen, key=Entscheidung.sortierschluessel)
    Path(pfad).parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, "w", encoding="utf-8", newline="\n") as f:
        for e in sortiert:
            f.write(json.dumps(asdict(e), ensure_ascii=False, sort_keys=True) + "\n")
    return len(sortiert)


def lesen(pfad: Path) -> list[Entscheidung]:
    with open(pfad, encoding="utf-8") as f:
        return [Entscheidung(**json.loads(z)) for z in f if z.strip()]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_korpus.py tests/test_leitplanke.py -v`
Expected: PASS — 7 Tests in `test_korpus.py`, 2 Tests in `test_leitplanke.py`; die beiden korpusabhängigen werden übersprungen.

- [ ] **Step 5: Commit**

```bash
git add src/doorway/korpus.py tests/test_korpus.py tests/test_leitplanke.py
git commit -m "feat: Korpus ohne Klarnamen, Leitplanke aus Paragraph 10 als Test"
```

---

### Task 8: Das Register — Aggregation mit Herkunft und Konflikterkennung

**Files:**
- Create: `src/doorway/register.py`
- Test: `tests/test_register.py`

**Interfaces:**
- Consumes: `doorway.korpus.Entscheidung`, `doorway.korpus.PROGRAMM`
- Produces: `Registerzeile` (frozen dataclass mit `programm, foerderelement, foerderjahr, bewilligungsstelle, antraege, bewilligt, abgelehnt, foerdervolumen_euro, ablehnungsgruende, herkunft, quelle_id, quelle_seite, konflikt`; Properties `schluessel`, `ablehnungsquote`), `zaehlen(entscheidungen) -> list[Registerzeile]`, `messen(zeilen, foerderjahr, quelle_id, achse) -> list[Registerzeile]`, `zusammenfuehren(gezaehlt, gemessen) -> list[Registerzeile]`, `als_csv(zeilen, pfad) -> int`, `als_json(zeilen, pfad) -> int`

Der Schlüssel ist `(programm, foerderelement, foerderjahr, bewilligungsstelle)`. `None` in einer der beiden mittleren Dimensionen bedeutet **„über alle"**, nicht „unbekannt".

- [ ] **Step 1: Write the failing test**

```python
# tests/test_register.py
import csv

from doorway.korpus import Entscheidung
from doorway.register import als_csv, messen, zaehlen, zusammenfuehren


def e(element="Heimat-Scheck", jahr=2025, status="bewilligt", grund=None, stelle=None):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        kommune="Ahlen",
        bezirksregierung=stelle,
        antragstellertyp=None,
        vorhabentext="Backhaus",
        betrag_euro="2000.00",
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=grund,
        quelle_id="vorl-18-5027",
        quelle_seite=16,
    )


def test_zaehlen_bildet_eine_zeile_je_element_jahr_und_stelle():
    zeilen = zaehlen(
        [e(), e(status="abgelehnt", grund="vereinsintern"), e(element="Heimat-Preis")]
    )
    assert len(zeilen) == 2
    scheck = next(z for z in zeilen if z.foerderelement == "Heimat-Scheck")
    assert (scheck.antraege, scheck.bewilligt, scheck.abgelehnt) == (2, 1, 1)


def test_zaehlen_setzt_herkunft_auf_gezaehlt():
    assert zaehlen([e()])[0].herkunft == "gezaehlt"


def test_zaehlen_sammelt_die_ablehnungsgruende_mit_haeufigkeit():
    zeilen = zaehlen(
        [
            e(status="abgelehnt", grund="vereinsintern"),
            e(status="abgelehnt", grund="vereinsintern"),
            e(status="abgelehnt", grund="entspricht nicht den Foerderkriterien"),
        ]
    )
    assert zeilen[0].ablehnungsgruende == {
        "vereinsintern": 2,
        "entspricht nicht den Foerderkriterien": 1,
    }


def test_die_ablehnungsquote_wird_aus_den_antraegen_berechnet():
    zeile = zaehlen([e(), e(status="abgelehnt", grund="x")])[0]
    assert zeile.ablehnungsquote == 0.5


def test_messen_uebernimmt_ein_aggregat_als_gemessen():
    zeilen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 1125,
                "bewilligt": 850,
                "abgelehnt": 275,
                "foerdervolumen_euro": "1700000.00",
                "seite": 9,
            }
        ],
        foerderjahr=2021,
        quelle_id="vorl-17-6633",
        achse="foerderelement",
    )
    assert zeilen[0].herkunft == "gemessen"
    assert zeilen[0].bewilligungsstelle is None
    assert zeilen[0].bewilligt == 850


def test_messen_auf_der_stellen_achse_laesst_das_element_offen():
    zeilen = messen(
        [
            {
                "bewilligungsstelle": "Koeln",
                "bewilligt": 134,
                "abgelehnt": 87,
                "foerdervolumen_euro": "551769.00",
                "seite": 6,
            }
        ],
        foerderjahr=2024,
        quelle_id="vorl-18-3926",
        achse="bewilligungsstelle",
    )
    assert zeilen[0].foerderelement is None
    assert zeilen[0].bewilligungsstelle == "Koeln"
    assert zeilen[0].antraege == 221


def test_zusammenfuehren_behaelt_gemessen_wenn_beide_uebereinstimmen():
    gezaehlt = zaehlen([e(), e()])
    gemessen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 2,
                "bewilligt": 2,
                "abgelehnt": 0,
                "foerdervolumen_euro": None,
                "seite": 1,
            }
        ],
        foerderjahr=2025,
        quelle_id="vorl-18-5027",
        achse="foerderelement",
    )
    ergebnis = zusammenfuehren(gezaehlt, gemessen)
    assert len(ergebnis) == 1
    assert ergebnis[0].herkunft == "gemessen"
    assert ergebnis[0].konflikt is None


def test_zusammenfuehren_meldet_konflikt_und_behaelt_beide_werte():
    gezaehlt = zaehlen([e(), e()])
    gemessen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 3,
                "bewilligt": 3,
                "abgelehnt": 0,
                "foerdervolumen_euro": None,
                "seite": 1,
            }
        ],
        foerderjahr=2025,
        quelle_id="vorl-18-5027",
        achse="foerderelement",
    )
    zeile = zusammenfuehren(gezaehlt, gemessen)[0]
    assert zeile.herkunft == "konflikt"
    assert zeile.konflikt == {
        "gemessen": {"antraege": 3, "bewilligt": 3, "abgelehnt": 0},
        "gezaehlt": {"antraege": 2, "bewilligt": 2, "abgelehnt": 0},
    }


def test_keine_registerzeile_hat_eine_leere_herkunft():
    for z in zusammenfuehren(zaehlen([e()]), []):
        assert z.herkunft in ("gemessen", "gezaehlt", "konflikt")


def test_als_csv_schreibt_die_herkunft_in_eine_eigene_spalte(tmp_path):
    datei = tmp_path / "register.csv"
    als_csv(zaehlen([e()]), datei)
    with open(datei, encoding="utf-8", newline="") as f:
        kopf = next(csv.reader(f, delimiter=";"))
    assert "herkunft" in kopf
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_register.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.register'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/register.py
"""Das Register: aggregiert je Programm, Förderelement, Jahr und Stelle.

Jede Zahl trägt ihre Herkunft (§13.2 der Spec). Widersprechen sich ein
genanntes Aggregat und die eigene Zählung, werden beide Werte behalten —
nie wird einer stillschweigend gewählt oder gemittelt.
"""

import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal

from .korpus import PROGRAMM, Entscheidung

Herkunft = Literal["gemessen", "gezaehlt", "konflikt"]

FELDER = ("antraege", "bewilligt", "abgelehnt")

SPALTEN = [
    "programm",
    "foerderelement",
    "foerderjahr",
    "bewilligungsstelle",
    "antraege",
    "bewilligt",
    "abgelehnt",
    "foerdervolumen_euro",
    "herkunft",
    "konflikt",
    "ablehnungsgruende",
    "quelle_id",
    "quelle_seite",
]


@dataclass(frozen=True)
class Registerzeile:
    programm: str
    foerderelement: str | None
    foerderjahr: int
    bewilligungsstelle: str | None
    antraege: int | None
    bewilligt: int | None
    abgelehnt: int | None
    foerdervolumen_euro: str | None
    ablehnungsgruende: dict[str, int]
    herkunft: Herkunft
    quelle_id: str
    quelle_seite: int
    konflikt: dict | None = None

    @property
    def schluessel(self) -> tuple:
        return (
            self.programm,
            self.foerderelement,
            self.foerderjahr,
            self.bewilligungsstelle,
        )

    @property
    def ablehnungsquote(self) -> float | None:
        if not self.antraege:
            return None
        return (self.abgelehnt or 0) / self.antraege


def _sortiert(zeilen: Iterable[Registerzeile]) -> list[Registerzeile]:
    return sorted(
        zeilen,
        key=lambda z: (z.foerderjahr, str(z.foerderelement), str(z.bewilligungsstelle)),
    )


def zaehlen(entscheidungen: Iterable[Entscheidung]) -> list[Registerzeile]:
    """Aggregiert Einzelentscheidungen zu Registerzeilen."""
    eimer: dict[tuple, list[Entscheidung]] = defaultdict(list)
    for e in entscheidungen:
        eimer[(e.programm, e.foerderelement, e.foerderjahr, e.bezirksregierung)].append(e)

    zeilen = []
    for (programm, element, jahr, stelle), gruppe in eimer.items():
        gruende = Counter(
            g.ablehnungsgrund_roh
            for g in gruppe
            if g.status == "abgelehnt" and g.ablehnungsgrund_roh
        )
        erste = gruppe[0]
        zeilen.append(
            Registerzeile(
                programm=programm,
                foerderelement=element,
                foerderjahr=jahr,
                bewilligungsstelle=stelle,
                antraege=len(gruppe),
                bewilligt=sum(1 for g in gruppe if g.status == "bewilligt"),
                abgelehnt=sum(1 for g in gruppe if g.status == "abgelehnt"),
                foerdervolumen_euro=None,
                ablehnungsgruende=dict(gruende.most_common()),
                herkunft="gezaehlt",
                quelle_id=erste.quelle_id,
                quelle_seite=erste.quelle_seite,
            )
        )
    return _sortiert(zeilen)


def messen(
    zeilen: Iterable[dict],
    foerderjahr: int,
    quelle_id: str,
    achse: Literal["foerderelement", "bewilligungsstelle"],
) -> list[Registerzeile]:
    """Übernimmt ein von der Quelle genanntes Aggregat unverändert.

    Fehlt die Antragszahl, wird sie aus bewilligt plus abgelehnt gebildet —
    das ist keine Schätzung, sondern eine Definition.
    """
    ergebnis = []
    for z in zeilen:
        bewilligt = z.get("bewilligt")
        abgelehnt = z.get("abgelehnt")
        antraege = z.get("antraege")
        if antraege is None and bewilligt is not None and abgelehnt is not None:
            antraege = bewilligt + abgelehnt
        ergebnis.append(
            Registerzeile(
                programm=PROGRAMM,
                foerderelement=(
                    z.get("foerderelement") if achse == "foerderelement" else None
                ),
                foerderjahr=foerderjahr,
                bewilligungsstelle=(
                    z.get("bewilligungsstelle") if achse == "bewilligungsstelle" else None
                ),
                antraege=antraege,
                bewilligt=bewilligt,
                abgelehnt=abgelehnt,
                foerdervolumen_euro=z.get("foerdervolumen_euro"),
                ablehnungsgruende={},
                herkunft="gemessen",
                quelle_id=quelle_id,
                quelle_seite=z["seite"],
            )
        )
    return ergebnis


def zusammenfuehren(
    gezaehlt: Iterable[Registerzeile], gemessen: Iterable[Registerzeile]
) -> list[Registerzeile]:
    """Führt gezählte und gemessene Zeilen zusammen und erkennt Konflikte."""
    nach_schluessel = {z.schluessel: z for z in gezaehlt}
    ergebnis: list[Registerzeile] = []
    verbraucht: set[tuple] = set()

    for m in gemessen:
        g = nach_schluessel.get(m.schluessel)
        if g is None:
            ergebnis.append(m)
            continue
        verbraucht.add(m.schluessel)
        felder = asdict(m)
        felder["ablehnungsgruende"] = g.ablehnungsgruende
        if all(getattr(m, f) == getattr(g, f) for f in FELDER):
            ergebnis.append(Registerzeile(**felder))
        else:
            felder["herkunft"] = "konflikt"
            felder["konflikt"] = {
                "gemessen": {f: getattr(m, f) for f in FELDER},
                "gezaehlt": {f: getattr(g, f) for f in FELDER},
            }
            ergebnis.append(Registerzeile(**felder))

    ergebnis += [z for s, z in nach_schluessel.items() if s not in verbraucht]
    return _sortiert(ergebnis)


def als_csv(zeilen: Iterable[Registerzeile], pfad: Path) -> int:
    zeilen = list(zeilen)
    Path(pfad).parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        schreiber = csv.DictWriter(f, fieldnames=SPALTEN, delimiter=";")
        schreiber.writeheader()
        for z in zeilen:
            d = asdict(z)
            d["konflikt"] = (
                json.dumps(d["konflikt"], ensure_ascii=False) if d["konflikt"] else ""
            )
            d["ablehnungsgruende"] = json.dumps(
                d["ablehnungsgruende"], ensure_ascii=False
            )
            schreiber.writerow({s: d[s] for s in SPALTEN})
    return len(zeilen)


def als_json(zeilen: Iterable[Registerzeile], pfad: Path) -> int:
    zeilen = list(zeilen)
    Path(pfad).parent.mkdir(parents=True, exist_ok=True)
    Path(pfad).write_text(
        json.dumps([asdict(z) for z in zeilen], ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    return len(zeilen)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_register.py -v`
Expected: PASS, 10 Tests

- [ ] **Step 5: Commit**

```bash
git add src/doorway/register.py tests/test_register.py
git commit -m "feat: Register mit Herkunftsspalte und Konflikterkennung"
```

---

### Task 9: Selbstwiderspruchs-Test — jedes Dokument gegen sich selbst

**Files:**
- Create: `src/doorway/genannt.py`
- Create: `golden/genannte-aggregate.json`
- Test: `tests/test_genannt.py`

**Interfaces:**
- Consumes: `doorway.register.Registerzeile`, `doorway.quellen.QUELLEN`
- Produces: `Genannt` (frozen dataclass mit `quelle_id: str`, `zitat: str`, `foerderjahr: int`, `foerderelement: str | None`, `bewilligungsstelle: str | None`, `bewilligt: int | None`, `abgelehnt: int | None`), `laden_genannte(pfad) -> list[Genannt]`, `normalisiert(text) -> str`, `seite_finden(pdf, zitat) -> int | None`, `vergleichen(genannte, register) -> list[dict]`

Dies ist Ebene 2 der Teststrategie aus §14.1: Jedes Dokument, das ein Aggregat **nennt** und zugleich eine Anlage **hat**, wird gegen sich selbst geprüft. Ohne diesen Task bliebe die Konflikt-Maschinerie aus Task 8 ungenutzt und der in der Spec zitierte Widerspruch (947 laut Bericht, 945 gezählt) eine Behauptung statt ein laufender Test.

**Der Beleg ist das Zitat, nicht die Seitenzahl.** Ein wörtliches Zitat lässt sich im PDF nachschlagen; eine Seitenzahl muss man glauben. Deshalb trägt jeder Eintrag den Originalwortlaut, und ein Test prüft, dass er im Quelldokument tatsächlich vorkommt.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_genannt.py
from pathlib import Path

import pytest

from doorway.genannt import (
    laden_genannte,
    normalisiert,
    seite_finden,
    vergleichen,
)
from doorway.laden import pfad
from doorway.quellen import quelle
from doorway.register import Registerzeile

GENANNTE = Path("golden/genannte-aggregate.json")


def r(element, jahr, bewilligt, abgelehnt):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende={},
        herkunft="gezaehlt",
        quelle_id="vorl-18-5027",
        quelle_seite=15,
    )


def test_normalisiert_zieht_zeilenumbrueche_zu_einzelnen_leerzeichen_zusammen():
    assert normalisiert("konnten  598\n Schecks") == "konnten 598 Schecks"


def test_die_kuratierte_datei_enthaelt_nur_bekannte_quellen():
    for g in laden_genannte(GENANNTE):
        assert g.quelle_id in {"vorl-18-5027", "vorl-18-3926"}


def test_jeder_eintrag_traegt_ein_zitat_und_mindestens_eine_zahl():
    for g in laden_genannte(GENANNTE):
        assert g.zitat.strip()
        assert g.bewilligt is not None or g.abgelehnt is not None


def test_vergleichen_findet_den_belegten_widerspruch_von_zwei_und_eins():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderelement == "Heimat-Scheck"
                and g.foerderjahr == 2025]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 596, 330)])
    treffer = [e for e in ergebnis if e["befund"] == "konflikt"]
    assert len(treffer) == 1
    assert treffer[0]["differenz"] == {"bewilligt": 2, "abgelehnt": -1}


def test_vergleichen_meldet_uebereinstimmung_wenn_die_zahlen_gleich_sind():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderelement == "Heimat-Scheck"
                and g.foerderjahr == 2025]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 598, 329)])
    assert [e["befund"] for e in ergebnis] == ["stimmt"]


def test_vergleichen_meldet_fehlendes_gegenstueck_statt_es_zu_verschweigen():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderjahr == 2024]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 596, 330)])
    assert [e["befund"] for e in ergebnis] == ["kein Gegenstueck"]


@pytest.mark.skipif(
    not pfad(quelle("vorl-18-5027"), Path("daten/quellen")).exists(),
    reason="Quelldokumente fehlen — erst `doorway laden` ausfuehren",
)
def test_jedes_zitat_steht_wirklich_im_quelldokument():
    fehlend = []
    for g in laden_genannte(GENANNTE):
        datei = pfad(quelle(g.quelle_id), Path("daten/quellen"))
        if seite_finden(datei, g.zitat) is None:
            fehlend.append((g.quelle_id, g.zitat))
    assert fehlend == [], f"Zitate nicht auffindbar: {fehlend}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_genannt.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.genannt'`

- [ ] **Step 3: Write the curated file of stated aggregates**

```json
[
 {
  "quelle_id": "vorl-18-5027",
  "zitat": "konnten 598",
  "foerderjahr": 2025,
  "foerderelement": "Heimat-Scheck",
  "bewilligungsstelle": null,
  "bewilligt": 598,
  "abgelehnt": null,
  "bemerkung": "Fliesstext: Im Foerderjahr 2025 konnten 598 Heimat-Schecks bewilligt werden (2024: 550)."
 },
 {
  "quelle_id": "vorl-18-5027",
  "zitat": "Zahl der Ablehnungen (329)",
  "foerderjahr": 2025,
  "foerderelement": "Heimat-Scheck",
  "bewilligungsstelle": null,
  "bewilligt": null,
  "abgelehnt": 329,
  "bemerkung": "Fliesstext: Die dennoch moeglichweise immer noch hoch erscheinende Zahl der Ablehnungen (329) hat vielfaeltige Gruende."
 },
 {
  "quelle_id": "vorl-18-3926",
  "zitat": "wurden 396 Antraege",
  "foerderjahr": 2024,
  "foerderelement": "Heimat-Scheck",
  "bewilligungsstelle": null,
  "bewilligt": null,
  "abgelehnt": 396,
  "bemerkung": "Fliesstext: Insgesamt wurden 396 Antraege auf die Bewilligung eines Heimat-Schecks durch die Bezirksregierungen abgelehnt. Fuer 2024 gibt es keine gezaehlte Gegenzeile — das Foerderjahr liegt nur als Aggregat je Bezirksregierung vor."
 }
]
```

Die beiden 2025er Einträge werden beim Vergleich zu **einer** Zeile zusammengefasst, weil sie denselben Schlüssel tragen: 598 bewilligt und 329 abgelehnt.

Hinweis zum Zitat `wurden 396 Antraege`: Im Original steht „Anträge" mit Umlaut. Der Vergleich normalisiert Umlaute nicht — schlägt `test_jedes_zitat_steht_wirklich_im_quelldokument` fehl, ist das Zitat auf den Originalwortlaut zu korrigieren, nicht der Test zu lockern.

- [ ] **Step 4: Write the implementation**

```python
# src/doorway/genannt.py
"""Ebene 2 der Teststrategie (§14.1): jedes Dokument gegen sich selbst.

Ein Bericht nennt im Fliesstext eine Zahl und liefert im Anhang die Zeilen,
aus denen sie entstanden sein soll. Beides muss zusammenpassen — und wo es
das nicht tut, gehoert die Differenz dokumentiert statt geglaettet.

Der Beleg ist das woertliche Zitat, nicht die Seitenzahl: Ein Zitat laesst
sich nachschlagen, eine Seitenzahl muss man glauben.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pymupdf

from .register import Registerzeile


@dataclass(frozen=True)
class Genannt:
    quelle_id: str
    zitat: str
    foerderjahr: int
    foerderelement: str | None
    bewilligungsstelle: str | None
    bewilligt: int | None
    abgelehnt: int | None
    bemerkung: str = ""

    @property
    def schluessel(self) -> tuple:
        return (self.foerderelement, self.foerderjahr, self.bewilligungsstelle)


def normalisiert(text: str) -> str:
    """Zieht alle Folgen von Leerraum zu einem einzelnen Leerzeichen zusammen."""
    return re.sub(r"\s+", " ", text).strip()


def laden_genannte(pfad: Path) -> list[Genannt]:
    roh = json.loads(Path(pfad).read_text(encoding="utf-8"))
    return [Genannt(**e) for e in roh]


def seite_finden(pdf: Path, zitat: str) -> int | None:
    """Seitenzahl (1-basiert), auf der das Zitat steht, oder None."""
    gesucht = normalisiert(zitat)
    dok = pymupdf.open(pdf)
    for i in range(dok.page_count):
        if gesucht in normalisiert(dok[i].get_text()):
            return i + 1
    return None


def vergleichen(
    genannte: Iterable[Genannt], register: Iterable[Registerzeile]
) -> list[dict]:
    """Vergleicht genannte Aggregate mit den gezaehlten Registerzeilen.

    Eintraege mit demselben Schluessel werden zusammengefasst — ein Bericht
    nennt die Bewilligungen und die Ablehnungen oft in getrennten Saetzen.
    """
    gebuendelt: dict[tuple, list[Genannt]] = defaultdict(list)
    for g in genannte:
        gebuendelt[g.schluessel].append(g)

    nach_schluessel = {
        (z.foerderelement, z.foerderjahr, z.bewilligungsstelle): z
        for z in register
        if z.herkunft == "gezaehlt"
    }

    ergebnis: list[dict] = []
    for schluessel, gruppe in gebuendelt.items():
        genannt_bewilligt = next((g.bewilligt for g in gruppe if g.bewilligt is not None), None)
        genannt_abgelehnt = next((g.abgelehnt for g in gruppe if g.abgelehnt is not None), None)
        zitate = [g.zitat for g in gruppe]
        zeile = nach_schluessel.get(schluessel)

        eintrag = {
            "foerderelement": schluessel[0],
            "foerderjahr": schluessel[1],
            "bewilligungsstelle": schluessel[2],
            "genannt": {"bewilligt": genannt_bewilligt, "abgelehnt": genannt_abgelehnt},
            "zitate": zitate,
            "quelle_id": gruppe[0].quelle_id,
        }

        if zeile is None:
            eintrag["befund"] = "kein Gegenstueck"
            eintrag["gezaehlt"] = None
            eintrag["differenz"] = None
            ergebnis.append(eintrag)
            continue

        eintrag["gezaehlt"] = {"bewilligt": zeile.bewilligt, "abgelehnt": zeile.abgelehnt}
        differenz = {
            feld: genannt - gezaehlt
            for feld, genannt, gezaehlt in (
                ("bewilligt", genannt_bewilligt, zeile.bewilligt),
                ("abgelehnt", genannt_abgelehnt, zeile.abgelehnt),
            )
            if genannt is not None and gezaehlt is not None
        }
        eintrag["differenz"] = differenz
        eintrag["befund"] = "stimmt" if all(d == 0 for d in differenz.values()) else "konflikt"
        ergebnis.append(eintrag)

    return ergebnis
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_genannt.py -v`
Expected: PASS, 7 Tests (der Zitat-Test wird übersprungen, wenn die PDFs fehlen)

- [ ] **Step 6: Run the real self-contradiction check**

Das Register wird hier bewusst inline gebaut: `doorway/cli.py` mit seiner Hilfsfunktion `_register_bauen` entsteht erst in Task 12, und dieser Task darf nicht vorgreifen.

```bash
python -c "
import json
from pathlib import Path
from doorway.genannt import laden_genannte, vergleichen
from doorway.korpus import aus_anlage_2025, aus_drucksache_2020
from doorway.register import zaehlen

alle = aus_anlage_2025(json.loads(Path('golden/vorl-18-5027.json').read_text(encoding='utf-8')))
alle += aus_drucksache_2020(json.loads(Path('golden/drs-17-9738.json').read_text(encoding='utf-8')))
register = zaehlen(alle)

for e in vergleichen(laden_genannte(Path('golden/genannte-aggregate.json')), register):
    print(e['befund'], '|', e['foerderelement'], e['foerderjahr'],
          '| genannt', e['genannt'], '| gezaehlt', e['gezaehlt'], '| Differenz', e['differenz'])
"
```

Expected: Eine Zeile `konflikt | Heimat-Scheck 2025 | genannt {'bewilligt': 598, 'abgelehnt': 329} | gezaehlt {'bewilligt': 596, 'abgelehnt': 330} | Differenz {'bewilligt': 2, 'abgelehnt': -1}` und eine Zeile `kein Gegenstueck | Heimat-Scheck 2024`.

Das ist der in §13.2 der Spec beschriebene Haarriss, jetzt als laufender Befund statt als Behauptung.

- [ ] **Step 7: Commit**

```bash
git add src/doorway/genannt.py golden/genannte-aggregate.json tests/test_genannt.py
git commit -m "feat: Selbstwiderspruchs-Test, jedes Dokument gegen sich selbst"
```

---

### Task 10: Stufe 1 — die Ausschlussregeln und ihre gemessene Treffsicherheit

**Files:**
- Create: `src/doorway/regeln.py`
- Create: `daten/korpus.jsonl` (im Schritt erzeugt)
- Test: `tests/test_regeln.py`

**Interfaces:**
- Consumes: `doorway.korpus.Entscheidung`, `doorway.korpus.lesen`
- Produces: `Regel` (frozen dataclass mit `name: str`, `beleg: str`, `hinweis: str`, `muster: re.Pattern | None`), `REGELN: tuple[Regel, ...]`, `pruefen(vorhabentext, antragstellertyp=None, mehrfachantrag=False) -> list[Regel]`, `treffsicherheit(regel, entscheidungen) -> tuple[int, int]`

**Das ist der Kern des Kill-Kriteriums.** Eine Regel darf nur feuern, wenn sie fast nie danebenliegt: Von allen Anträgen, auf die sie zutrifft, dürfen höchstens 1 % bewilligt worden sein. `treffsicherheit` misst das gegen den Korpus; der Test schaltet jede Regel ab, die reißt.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_regeln.py
from pathlib import Path

import pytest

from doorway.korpus import Entscheidung, lesen
from doorway.regeln import REGELN, pruefen, treffsicherheit

KORPUS = Path("daten/korpus.jsonl")


def e(text, status="abgelehnt"):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=2025,
        kommune="Ahlen",
        bezirksregierung=None,
        antragstellertyp=None,
        vorhabentext=text,
        betrag_euro=None,
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=None,
        quelle_id="vorl-18-5027",
        quelle_seite=1,
    )


def test_jede_regel_traegt_einen_beleg():
    for r in REGELN:
        assert r.beleg, f"Regel {r.name} ohne Beleg"
        assert "Drs" in r.beleg or "Vorl" in r.beleg


def test_trikots_loesen_die_ausstattungsregel_aus():
    assert [r.name for r in pruefen("Neue Trikots fuer die Jugendmannschaft")] == [
        "vereinseigene Ausstattung"
    ]


def test_eine_vereinsfahne_loest_die_ausstattungsregel_aus():
    assert [r.name for r in pruefen("Restaurierung Vereinsfahne")] == [
        "vereinseigene Ausstattung"
    ]


def test_eine_firma_ist_nicht_antragsberechtigt():
    assert [
        r.name for r in pruefen("Digitalisierung des Ortsarchivs", antragstellertyp="Firma")
    ] == ["fehlende Antragsberechtigung"]


def test_der_zweite_antrag_im_jahr_loest_die_mehrfachregel_aus():
    assert [
        r.name for r in pruefen("Digitalisierung des Ortsarchivs", mehrfachantrag=True)
    ] == ["Mehrfachantrag im Foerderjahr"]


def test_ein_unauffaelliges_vorhaben_loest_keine_regel_aus():
    assert pruefen("Digitalisierung des Ortsarchivs") == []


def test_ein_museumsprojekt_loest_keine_regel_aus():
    assert pruefen("Sonderausstellung zur Geschichte der Gesangvereine") == []


def test_treffsicherheit_zaehlt_treffer_und_fehltreffer():
    entscheidungen = [
        e("Neue Trikots"),
        e("Neue Trikots", status="bewilligt"),
        e("Digitalisierung"),
    ]
    regel = next(r for r in REGELN if r.name == "vereinseigene Ausstattung")
    assert treffsicherheit(regel, entscheidungen) == (2, 1)


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_keine_regel_reisst_die_ein_prozent_huerde():
    """Das Kill-Kriterium aus Paragraph 14.2, Huerde 1 — auf Regelebene."""
    entscheidungen = lesen(KORPUS)
    gerissen = []
    for r in REGELN:
        getroffen, faelschlich = treffsicherheit(r, entscheidungen)
        if getroffen == 0:
            continue
        quote = faelschlich / getroffen
        if quote > 0.01:
            gerissen.append(f"{r.name}: {faelschlich}/{getroffen} = {quote:.1%}")
    assert gerissen == [], "Regeln ueber der 1-Prozent-Huerde: " + "; ".join(gerissen)


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_jede_gemusterte_regel_findet_im_korpus_ueberhaupt_etwas():
    """Eine Regel, die nie feuert, ist Ballast und gehoert entfernt."""
    entscheidungen = lesen(KORPUS)
    stumm = [
        r.name
        for r in REGELN
        if r.muster is not None and treffsicherheit(r, entscheidungen)[0] == 0
    ]
    assert stumm == [], f"Regeln ohne einen einzigen Treffer: {stumm}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_regeln.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.regeln'`

- [ ] **Step 3: Write the rule engine**

```python
# src/doorway/regeln.py
"""Stufe 1 der Prognose: die Ausschlussprüfung (§12.1 der Spec).

Die Ablehnungen der Heimatförderung sind kategorisch, nicht graduell. Wer
Vereinstrikots beantragt, hat keine 38-Prozent-Chance, sondern null. Diese
Stufe erkennt die belegten Ausschlussgründe, bevor überhaupt gerechnet wird.

Jede Regel muss die 1-Prozent-Hürde aus §14.2 halten: Von allen Anträgen,
auf die sie zutrifft, dürfen höchstens ein Prozent bewilligt worden sein.
Gemessen wird das in tests/test_regeln.py gegen den Korpus. Eine Regel, die
reißt, wird enger gefasst oder entfernt — nicht die Hürde gelockert.
"""

import re
from dataclasses import dataclass
from typing import Iterable

from .korpus import Entscheidung


@dataclass(frozen=True)
class Regel:
    name: str
    beleg: str
    hinweis: str
    muster: re.Pattern | None = None


REGELN: tuple[Regel, ...] = (
    Regel(
        name="vereinseigene Ausstattung",
        beleg="Drs 17/9738 (Ablehnungsgruende 2018-2019); Vorl 18/5027, Foerderjahr 2025",
        hinweis="Ausstattung, die dem Verein selbst gehoert und ihm allein nuetzt, "
        "ist nicht foerderfaehig — Trikots, Uniformen, Fahnen, Mobiliar.",
        muster=re.compile(
            r"\btrikot|\buniform|vereinsfahne|vereinskleidung|dienstkleidung",
            re.IGNORECASE,
        ),
    ),
    Regel(
        name="fehlende Antragsberechtigung",
        beleg="Vorl 18/5027, Foerderjahr 2025",
        hinweis="Antragsberechtigt sind Vereine, Initiativen, Stiftungen, Kommunen "
        "und Privatpersonen — keine Unternehmen.",
    ),
    Regel(
        name="Mehrfachantrag im Foerderjahr",
        beleg="Vorl 18/5027, Foerderjahr 2025 (Foerderrichtlinie: ein Scheck je Jahr "
        "und Antragstellendem)",
        hinweis="Pro Foerderjahr ist nur ein Heimat-Scheck je Antragstellendem moeglich.",
    ),
)


def pruefen(
    vorhabentext: str | None,
    antragstellertyp: str | None = None,
    mehrfachantrag: bool = False,
) -> list[Regel]:
    """Gibt die Regeln zurück, die diesem Vorhaben im Weg stehen."""
    getroffen = []
    for r in REGELN:
        if r.muster is not None:
            if vorhabentext and r.muster.search(vorhabentext):
                getroffen.append(r)
        elif r.name == "fehlende Antragsberechtigung" and antragstellertyp == "Firma":
            getroffen.append(r)
        elif r.name == "Mehrfachantrag im Foerderjahr" and mehrfachantrag:
            getroffen.append(r)
    return getroffen


def treffsicherheit(
    regel: Regel, entscheidungen: Iterable[Entscheidung]
) -> tuple[int, int]:
    """Misst eine Regel am Korpus.

    Gibt (getroffen, faelschlich) zurück: wie viele Anträge das Muster trifft
    und wie viele davon tatsächlich bewilligt wurden. Der zweite Wert ist die
    Zahl der Menschen, denen Doorway zu Unrecht abgeraten hätte.
    """
    if regel.muster is None:
        return (0, 0)
    getroffen = [
        e
        for e in entscheidungen
        if e.vorhabentext and regel.muster.search(e.vorhabentext)
    ]
    return (len(getroffen), sum(1 for e in getroffen if e.status == "bewilligt"))
```

- [ ] **Step 4: Run the unit tests**

Run: `python -m pytest tests/test_regeln.py -v`
Expected: PASS, 8 Tests; die beiden korpusabhängigen werden übersprungen.

- [ ] **Step 5: Harvest the corpus so the measured tests can run**

```bash
python -c "
import json
from pathlib import Path
from doorway.korpus import aus_anlage_2025, aus_drucksache_2020, schreiben
alle = aus_anlage_2025(json.loads(Path('golden/vorl-18-5027.json').read_text(encoding='utf-8')))
alle += aus_drucksache_2020(json.loads(Path('golden/drs-17-9738.json').read_text(encoding='utf-8')))
print(schreiben(alle, Path('daten/korpus.jsonl')), 'Entscheidungen im Korpus')
"
```

Expected: rund 4.600 Entscheidungen — 1.296 aus dem Förderjahr 2025 und rund 3.310 aus 2018/2019 (Zeilen ohne Antragsdatum entfallen).

- [ ] **Step 6: Run the measured tests — the first real reading of the kill criterion**

Run: `python -m pytest tests/test_regeln.py tests/test_leitplanke.py -v`
Expected: PASS, alle Tests.

**Schlägt `test_keine_regel_reisst_die_ein_prozent_huerde` fehl, ist das kein Testfehler.** Die Meldung nennt Regel und Quote. Dann gilt §14.2: Muster enger fassen oder Regel entfernen — die Hürde bleibt bei 1 %.

**Schlägt `test_jede_gemusterte_regel_findet_im_korpus_ueberhaupt_etwas` fehl**, feuert ein Muster nie. Es ist entweder falsch geschrieben oder überflüssig; beides gehört behoben, bevor weitergebaut wird.

- [ ] **Step 7: Commit**

```bash
git add src/doorway/regeln.py tests/test_regeln.py daten/korpus.jsonl
git commit -m "feat: Stufe 1 der Prognose, Regeln mit gemessener Treffsicherheit"
```

---

### Task 11: Stufe 2 — Basisrate mit Intervall aus der Regimeschwankung

**Files:**
- Create: `src/doorway/basisrate.py`
- Test: `tests/test_basisrate.py`

**Interfaces:**
- Consumes: `doorway.register.Registerzeile`
- Produces: `Z95: float`, `Schaetzung` (frozen dataclass mit `quote: float`, `halbe_breite: float`, `grundlage_n: int`, `jahre: tuple[int, ...]`, `quelle_id: str`; Properties `chance`, `untergrenze`, `obergrenze`), `reihe(register, foerderelement, bewilligungsstelle=None) -> list[Registerzeile]`, `schaetzen(register, foerderelement, bewilligungsstelle=None, bis_jahr=None) -> Schaetzung | None`

**Der zentrale Befund aus §12.3:** Die Unsicherheit wird von der Schwankung zwischen den Förderjahren bestimmt, nicht vom Stichprobenfehler. Ausgewiesen wird immer die größere der beiden Größen.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_basisrate.py
import math

from doorway.basisrate import schaetzen
from doorway.register import Registerzeile


def r(jahr, bewilligt, abgelehnt, element="Heimat-Scheck", stelle=None):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        bewilligungsstelle=stelle,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende={},
        herkunft="gezaehlt",
        quelle_id="test",
        quelle_seite=1,
    )


BELEGT = [
    r(2018, 814, 469),
    r(2019, 996, 659),
    r(2021, 850, 275),
    r(2024, 550, 396),
    r(2025, 596, 330),
]


def test_die_schaetzung_nimmt_das_juengste_belegte_jahr_als_punktwert():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.quote == 330 / 926
    assert s.grundlage_n == 926


def test_das_intervall_folgt_der_jahresschwankung_nicht_dem_stichprobenfehler():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    p, n = 330 / 926, 926
    stichprobe = 1.96 * math.sqrt(p * (1 - p) / n)
    assert s.halbe_breite > stichprobe * 3


def test_das_intervall_deckt_die_beobachtete_spannweite_weitgehend_ab():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.untergrenze < 0.244
    assert s.obergrenze > 0.419


def test_bei_nur_einem_jahr_bleibt_der_stichprobenfehler_uebrig():
    s = schaetzen([r(2025, 596, 330)], "Heimat-Scheck")
    p, n = 330 / 926, 926
    assert s.halbe_breite == 1.96 * math.sqrt(p * (1 - p) / n)


def test_bis_jahr_blendet_spaetere_jahre_aus_fuer_den_backtest():
    s = schaetzen(BELEGT, "Heimat-Scheck", bis_jahr=2021)
    assert s.quote == 275 / 1125
    assert 2024 not in s.jahre


def test_ein_element_ohne_daten_liefert_keine_schaetzung():
    assert schaetzen(BELEGT, "Heimat-Werkstatt") is None


def test_die_stelle_wird_beruecksichtigt_wenn_sie_angegeben_ist():
    mit_stelle = BELEGT + [r(2024, 134, 87, stelle="Koeln")]
    s = schaetzen(mit_stelle, "Heimat-Scheck", bewilligungsstelle="Koeln")
    assert s.quote == 87 / 221


def test_die_schaetzung_nennt_die_jahre_auf_denen_sie_beruht():
    assert schaetzen(BELEGT, "Heimat-Scheck").jahre == (2018, 2019, 2021, 2024, 2025)


def test_chance_ist_die_gegenwahrscheinlichkeit_der_quote():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.chance == 1.0 - s.quote
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_basisrate.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.basisrate'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/basisrate.py
"""Stufe 2 der Prognose: die Basisrate (§12.2 und §12.3 der Spec).

Der Punktwert kommt aus dem jüngsten belegten Förderjahr. Das Intervall
kommt aus der Schwankung zwischen den Jahren, nicht aus dem Stichprobenfehler:
Die Ablehnungsquote des Heimat-Schecks schwankte zwischen 24,4 und 41,9
Prozent, während der Stichprobenfehler bei rund drei Punkten liegt. Wer nur
die Stichprobe ausweist, ist um den Faktor vier zu selbstsicher.
"""

import math
import statistics
from dataclasses import dataclass
from typing import Iterable

from .register import Registerzeile

Z95 = 1.96


@dataclass(frozen=True)
class Schaetzung:
    quote: float
    halbe_breite: float
    grundlage_n: int
    jahre: tuple[int, ...]
    quelle_id: str

    @property
    def chance(self) -> float:
        return 1.0 - self.quote

    @property
    def untergrenze(self) -> float:
        return max(0.0, self.quote - self.halbe_breite)

    @property
    def obergrenze(self) -> float:
        return min(1.0, self.quote + self.halbe_breite)


def reihe(
    register: Iterable[Registerzeile],
    foerderelement: str,
    bewilligungsstelle: str | None = None,
) -> list[Registerzeile]:
    """Alle Registerzeilen für dieses Element und diese Stelle, nach Jahr sortiert."""
    passend = [
        z
        for z in register
        if z.foerderelement == foerderelement
        and z.bewilligungsstelle == bewilligungsstelle
        and z.antraege
        and z.abgelehnt is not None
    ]
    return sorted(passend, key=lambda z: z.foerderjahr)


def schaetzen(
    register: Iterable[Registerzeile],
    foerderelement: str,
    bewilligungsstelle: str | None = None,
    bis_jahr: int | None = None,
) -> Schaetzung | None:
    """Schätzt die Ablehnungsquote samt ehrlichem Intervall.

    `bis_jahr` blendet spätere Jahre aus — so rechnet der Backtest mit dem
    Wissensstand von damals.
    """
    zeilen = reihe(register, foerderelement, bewilligungsstelle)
    if bis_jahr is not None:
        zeilen = [z for z in zeilen if z.foerderjahr <= bis_jahr]
    if not zeilen:
        return None

    juengste = zeilen[-1]
    quote = juengste.abgelehnt / juengste.antraege
    n = juengste.antraege

    stichprobenfehler = Z95 * math.sqrt(quote * (1 - quote) / n)
    quoten = [z.abgelehnt / z.antraege for z in zeilen]
    regime = Z95 * statistics.stdev(quoten) if len(quoten) >= 2 else 0.0

    return Schaetzung(
        quote=quote,
        halbe_breite=max(stichprobenfehler, regime),
        grundlage_n=n,
        jahre=tuple(z.foerderjahr for z in zeilen),
        quelle_id=juengste.quelle_id,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_basisrate.py -v`
Expected: PASS, 9 Tests

- [ ] **Step 5: Commit**

```bash
git add src/doorway/basisrate.py tests/test_basisrate.py
git commit -m "feat: Stufe 2 mit Intervall aus der Regimeschwankung statt aus der Stichprobe"
```

---

### Task 12: Die Prognose — beide Stufen in einem Panel, und `doorway prognose`

**Files:**
- Create: `src/doorway/prognose.py`
- Create: `src/doorway/cli.py`
- Create: `daten/register.csv`, `daten/register.json` (im Schritt erzeugt)
- Test: `tests/test_prognose.py`

**Interfaces:**
- Consumes: `doorway.regeln.REGELN`, `doorway.regeln.pruefen`, `doorway.basisrate.schaetzen`, `doorway.register.Registerzeile`
- Produces: `Urteil` (frozen dataclass mit `chancenlos: bool`, `regeln: list[Regel]`, `schaetzung: Schaetzung | None`, `bestanden: list[str]`, `gruende: dict[str, int]`, `beleg: str`), `beurteilen(register, vorhabentext, foerderelement, bewilligungsstelle=None, antragstellertyp=None, mehrfachantrag=False) -> Urteil`, `panel(urteil, vorhabentext, foerderelement, bewilligungsstelle) -> str`
- Produces (CLI): `main(argv=None) -> int` mit den Unterbefehlen `laden`, `ernten`, `prognose`; Hilfsfunktion `_register_bauen() -> list[Registerzeile]`, die auch Task 13 verwendet

Gleiche Form in beiden Fällen (§12.4): Kopf, Urteilszeile, vollständige Ausschlussprüfung, Gründeverteilung, Belegzeile. Die Ausschlussprüfung steht immer da, auch wenn alles bestanden ist.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_prognose.py
from doorway.prognose import beurteilen, panel
from doorway.register import Registerzeile


def r(jahr, bewilligt, abgelehnt, gruende=None):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende=gruende or {},
        herkunft="gezaehlt",
        quelle_id="vorl-18-5027",
        quelle_seite=15,
    )


REGISTER = [
    r(2018, 814, 469),
    r(2019, 996, 659),
    r(2021, 850, 275),
    r(2024, 550, 396),
    r(
        2025,
        596,
        330,
        {"entspricht nicht den Foerderkriterien": 277, "vereinsuebliche Ausstattung": 23},
    ),
]


def test_ein_trikotantrag_ist_chancenlos_und_bekommt_keine_prozentzahl():
    u = beurteilen(REGISTER, "Neue Trikots fuer den Schuetzenverein", "Heimat-Scheck")
    assert u.chancenlos is True
    assert [x.name for x in u.regeln] == ["vereinseigene Ausstattung"]


def test_ein_unauffaelliges_vorhaben_bekommt_eine_schaetzung():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert u.chancenlos is False
    assert u.schaetzung is not None
    assert 0.0 < u.schaetzung.quote < 1.0


def test_das_urteil_nennt_auch_die_bestandenen_pruefungen():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert set(u.bestanden) == {
        "vereinseigene Ausstattung",
        "fehlende Antragsberechtigung",
        "Mehrfachantrag im Foerderjahr",
    }


def test_das_panel_zeigt_die_ausschlusspruefung_auch_im_guten_fall():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    text = panel(u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None)
    assert "Ausschlusspruefung" in text
    assert "3 von 3 bestanden" in text


def test_das_panel_nennt_im_schlechten_fall_die_regel_statt_einer_zahl():
    u = beurteilen(REGISTER, "Neue Trikots", "Heimat-Scheck")
    text = panel(u, "Neue Trikots", "Heimat-Scheck", None)
    assert "Chance nahe null" in text
    assert "vereinseigene Ausstattung" in text
    assert "%" not in text.split("Woran es hier scheitert")[0]


def test_das_panel_traegt_immer_eine_belegzeile():
    for vorhaben in ("Neue Trikots", "Ortsarchiv digitalisieren"):
        u = beurteilen(REGISTER, vorhaben, "Heimat-Scheck")
        assert "Beleg" in panel(u, vorhaben, "Heimat-Scheck", None)


def test_das_panel_weist_die_unsicherheit_aus():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert "+/-" in panel(u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None)


def test_ohne_registerdaten_gibt_es_keine_erfundene_zahl():
    u = beurteilen([], "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert u.schaetzung is None
    assert "keine belegten Zahlen" in panel(
        u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_prognose.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.prognose'`

- [ ] **Step 3: Write the prognosis**

```python
# src/doorway/prognose.py
"""Die Prognose: zweistufig gerechnet, einstufig angezeigt (§12 der Spec).

Die Regelprüfung entscheidet, welche Zeile das Gewicht trägt — sie erzeugt
keinen zweiten Bildschirm. Beide Fälle bekommen dasselbe Panel in derselben
Anordnung, damit das Auge nach dem zweiten Mal weiß, wo es hinschauen muss.
"""

from dataclasses import dataclass
from typing import Iterable

from .basisrate import Schaetzung, schaetzen
from .regeln import REGELN, Regel, pruefen
from .register import Registerzeile

BREITE = 70


@dataclass(frozen=True)
class Urteil:
    chancenlos: bool
    regeln: list[Regel]
    schaetzung: Schaetzung | None
    bestanden: list[str]
    gruende: dict[str, int]
    beleg: str


def beurteilen(
    register: Iterable[Registerzeile],
    vorhabentext: str,
    foerderelement: str,
    bewilligungsstelle: str | None = None,
    antragstellertyp: str | None = None,
    mehrfachantrag: bool = False,
) -> Urteil:
    register = list(register)
    getroffen = pruefen(vorhabentext, antragstellertyp, mehrfachantrag)
    namen = {r.name for r in getroffen}
    bestanden = [r.name for r in REGELN if r.name not in namen]

    schaetzung = schaetzen(register, foerderelement, bewilligungsstelle)
    mit_gruenden = [
        z
        for z in register
        if z.foerderelement == foerderelement
        and z.bewilligungsstelle == bewilligungsstelle
        and z.ablehnungsgruende
    ]
    gruende = mit_gruenden[-1].ablehnungsgruende if mit_gruenden else {}
    if mit_gruenden:
        beleg = f"{mit_gruenden[-1].quelle_id}, Seite {mit_gruenden[-1].quelle_seite}"
    elif schaetzung:
        beleg = schaetzung.quelle_id
    else:
        beleg = "keine Quelle"

    return Urteil(
        chancenlos=bool(getroffen),
        regeln=getroffen,
        schaetzung=schaetzung,
        bestanden=bestanden,
        gruende=gruende,
        beleg=beleg,
    )


def _zeile(text: str = "") -> str:
    return "| " + text[: BREITE - 4].ljust(BREITE - 4) + " |"


def panel(
    urteil: Urteil,
    vorhabentext: str,
    foerderelement: str,
    bewilligungsstelle: str | None,
) -> str:
    """Formt das Urteil als Textpanel — gleiche Form in beiden Fällen."""
    kopf = "CHANCENLOS" if urteil.chancenlos else "AUSSICHTSREICH"
    stelle = bewilligungsstelle or "landesweit"
    zeilen = [
        "+- " + kopf + " " + "-" * (BREITE - len(kopf) - 5) + "+",
        _zeile(vorhabentext),
        _zeile(f"{foerderelement} · {stelle}"),
        _zeile(),
    ]

    if urteil.chancenlos:
        r = urteil.regeln[0]
        zeilen += [
            _zeile("  X  Chance nahe null"),
            _zeile(f"     {r.name}"),
            _zeile(f"     {r.hinweis}"),
        ]
    elif urteil.schaetzung is None:
        zeilen += [_zeile("  ?  Fuer diese Kombination gibt es keine belegten Zahlen.")]
    else:
        s = urteil.schaetzung
        zeilen += [
            _zeile(f"  OK Chance rund {s.chance:.0%}      +/- {s.halbe_breite:.0%}"),
            _zeile(
                f"     Basis: {s.grundlage_n} Antraege, "
                f"Foerderjahre {s.jahre[0]}-{s.jahre[-1]}"
            ),
        ]

    zeilen += [
        _zeile(),
        _zeile(f"Ausschlusspruefung        {len(urteil.bestanden)} von {len(REGELN)} bestanden"),
    ]
    for r in REGELN:
        haken = "+" if r.name in urteil.bestanden else "X"
        zeilen.append(_zeile(f"  {haken} {r.name}"))

    if urteil.gruende:
        gesamt = sum(urteil.gruende.values())
        zeilen += [_zeile(), _zeile("Woran es hier scheitert")]
        for grund, anzahl in list(urteil.gruende.items())[:4]:
            marke = ""
            if urteil.chancenlos and urteil.regeln[0].name.lower()[:12] in grund.lower():
                marke = "  <- dein Fall"
            zeilen.append(_zeile(f"  {grund[:38]:<38} {anzahl / gesamt:>5.0%}{marke}"))

    zeilen += [_zeile(), _zeile(f"Beleg  {urteil.beleg}")]
    zeilen.append("+" + "-" * (BREITE - 2) + "+")
    return "\n".join(zeilen)
```

- [ ] **Step 4: Write the command line entry point**

```python
# src/doorway/cli.py
"""Einstiegspunkt: doorway <befehl>."""

import argparse
import json
import sys
from pathlib import Path

from . import korpus as k
from . import register as reg
from .laden import laden, lock_pruefen, lock_schreiben
from .prognose import beurteilen, panel
from .quellen import QUELLEN

QUELLVERZEICHNIS = Path("daten/quellen")
LOCK = Path("daten/quellen.lock.json")
KORPUS = Path("daten/korpus.jsonl")
REGISTER_CSV = Path("daten/register.csv")
REGISTER_JSON = Path("daten/register.json")
GOLDEN = Path("golden")


def _laden(_args) -> int:
    for q in QUELLEN.values():
        print(q.id, laden(q, QUELLVERZEICHNIS))
    if LOCK.exists():
        abweichend = lock_pruefen(QUELLVERZEICHNIS, LOCK)
        if abweichend:
            print("Pruefsumme abweichend:", ", ".join(abweichend), file=sys.stderr)
            return 1
    else:
        lock_schreiben(QUELLVERZEICHNIS, LOCK)
    return 0


def _register_bauen() -> list[reg.Registerzeile]:
    gezaehlt = reg.zaehlen(k.lesen(KORPUS))
    gemessen = reg.messen(
        json.loads((GOLDEN / "vorl-17-6633.json").read_text(encoding="utf-8")),
        foerderjahr=2021,
        quelle_id="vorl-17-6633",
        achse="foerderelement",
    ) + reg.messen(
        json.loads((GOLDEN / "vorl-18-3926.json").read_text(encoding="utf-8")),
        foerderjahr=2024,
        quelle_id="vorl-18-3926",
        achse="bewilligungsstelle",
    )
    return reg.zusammenfuehren(gezaehlt, gemessen)


def _ernten(_args) -> int:
    alle = k.aus_anlage_2025(
        json.loads((GOLDEN / "vorl-18-5027.json").read_text(encoding="utf-8"))
    ) + k.aus_drucksache_2020(
        json.loads((GOLDEN / "drs-17-9738.json").read_text(encoding="utf-8"))
    )
    print(k.schreiben(alle, KORPUS), "Entscheidungen im Korpus")
    zeilen = _register_bauen()
    reg.als_csv(zeilen, REGISTER_CSV)
    reg.als_json(zeilen, REGISTER_JSON)
    konflikte = sum(1 for z in zeilen if z.herkunft == "konflikt")
    print(len(zeilen), "Registerzeilen,", konflikte, "davon mit Konflikt")
    return 0


def _prognose(args) -> int:
    urteil = beurteilen(
        _register_bauen(),
        args.vorhaben,
        args.element,
        bewilligungsstelle=args.stelle,
        antragstellertyp=args.typ,
        mehrfachantrag=args.mehrfachantrag,
    )
    print(panel(urteil, args.vorhaben, args.element, args.stelle))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="doorway")
    unter = p.add_subparsers(dest="befehl", required=True)

    unter.add_parser("laden", help="Quelldokumente holen und pruefen").set_defaults(fn=_laden)
    unter.add_parser("ernten", help="Korpus und Register neu bauen").set_defaults(fn=_ernten)

    pr = unter.add_parser("prognose", help="Prognose fuer ein Vorhaben")
    pr.add_argument("vorhaben")
    pr.add_argument("--element", default="Heimat-Scheck")
    pr.add_argument("--stelle", default=None)
    pr.add_argument("--typ", default=None)
    pr.add_argument("--mehrfachantrag", action="store_true")
    pr.set_defaults(fn=_prognose)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_prognose.py -v`
Expected: PASS, 8 Tests

- [ ] **Step 6: Build the register and try both cases by hand**

```bash
python -m doorway.cli ernten
python -m doorway.cli prognose "Neue Trikots fuer den Schuetzenverein"
python -m doorway.cli prognose "Ortsarchiv digitalisieren"
```

Expected: Das erste Panel trägt „Chance nahe null" und die Regel `vereinseigene Ausstattung`, das zweite eine Prozentzahl mit Intervall. Beide zeigen die vollständige Ausschlussprüfung und eine Belegzeile.

- [ ] **Step 7: Commit**

```bash
git add src/doorway/prognose.py src/doorway/cli.py tests/test_prognose.py daten/register.csv daten/register.json
git commit -m "feat: Prognose-Panel und Kommandozeile fuer Ernte und Auskunft"
```

---

### Task 13: Der Backtest und das Kill-Kriterium

**Files:**
- Create: `src/doorway/backtest.py`
- Modify: `src/doorway/cli.py` (Unterbefehl `kill-kriterium` ergänzen)
- Test: `tests/test_backtest.py`

**Interfaces:**
- Consumes: `doorway.basisrate.schaetzen`, `doorway.regeln.REGELN`, `doorway.regeln.treffsicherheit`, `doorway.korpus.Entscheidung`, `doorway.register.Registerzeile`
- Produces: `GRENZE_FALSCHE_ABSAGEN: float`, `Vorhersage` (frozen dataclass mit `foerderelement`, `jahr`, `vorhergesagt`, `tatsaechlich`, `halbe_breite`; Property `getroffen`), `Bericht` (frozen dataclass mit `absagen`, `vorhersagen`, `huerde_absagen_bestanden`, `huerde_kalibrierung_bestanden`; Property `bestanden`), `kalibrierung(register) -> list[Vorhersage]`, `absagen(entscheidungen) -> list[tuple[str, int, int]]`, `pruefen(register, entscheidungen) -> Bericht`, `als_text(bericht) -> str`

Der Backtest sagt jedes Förderjahr aus den *davor* liegenden vorher und prüft, ob die tatsächliche Quote im ausgewiesenen Intervall liegt. Er misst nicht, wie klein der Fehler ist, sondern ob die Prognose überrascht wurde.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_backtest.py
from pathlib import Path

import pytest

from doorway.backtest import als_text, kalibrierung, pruefen
from doorway.korpus import Entscheidung
from doorway.register import Registerzeile

KORPUS = Path("daten/korpus.jsonl")


def r(jahr, bewilligt, abgelehnt):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende={},
        herkunft="gezaehlt",
        quelle_id="test",
        quelle_seite=1,
    )


BELEGT = [
    r(2018, 814, 469),
    r(2019, 996, 659),
    r(2021, 850, 275),
    r(2024, 550, 396),
    r(2025, 596, 330),
]


def e(status):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=2025,
        kommune=None,
        bezirksregierung=None,
        antragstellertyp=None,
        vorhabentext="Neue Trikots",
        betrag_euro=None,
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=None,
        quelle_id="test",
        quelle_seite=1,
    )


def test_das_erste_jahr_wird_nicht_vorhergesagt():
    assert 2018 not in [v.jahr for v in kalibrierung(BELEGT)]


def test_jedes_spaetere_jahr_wird_vorhergesagt():
    assert [v.jahr for v in kalibrierung(BELEGT)] == [2019, 2021, 2024, 2025]


def test_eine_vorhersage_gilt_als_getroffen_wenn_sie_im_intervall_liegt():
    for v in kalibrierung(BELEGT):
        assert v.getroffen == (
            v.vorhergesagt - v.halbe_breite
            <= v.tatsaechlich
            <= v.vorhergesagt + v.halbe_breite
        )


def test_der_bericht_nennt_beide_huerden():
    bericht = pruefen(BELEGT, [])
    assert hasattr(bericht, "huerde_absagen_bestanden")
    assert hasattr(bericht, "huerde_kalibrierung_bestanden")


def test_bestanden_ist_nur_wahr_wenn_beide_huerden_halten():
    bericht = pruefen(BELEGT, [])
    assert bericht.bestanden == (
        bericht.huerde_absagen_bestanden and bericht.huerde_kalibrierung_bestanden
    )


def test_eine_falsche_absage_ueber_ein_prozent_reisst_die_erste_huerde():
    treffer = [e("abgelehnt")] * 50 + [e("bewilligt")] * 5
    assert pruefen(BELEGT, treffer).huerde_absagen_bestanden is False


def test_wenige_falsche_absagen_unter_ein_prozent_reissen_nicht():
    treffer = [e("abgelehnt")] * 200 + [e("bewilligt")]
    assert pruefen(BELEGT, treffer).huerde_absagen_bestanden is True


def test_der_text_nennt_bei_konflikt_den_vorrang_der_absage():
    assert "Bei Konflikt gewinnt die Absage" in als_text(pruefen(BELEGT, []))


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_der_echte_lauf_erzeugt_einen_lesbaren_bericht():
    from doorway.cli import _register_bauen
    from doorway.korpus import lesen

    text = als_text(pruefen(_register_bauen(), lesen(KORPUS)))
    assert "Huerde 1" in text and "Huerde 2" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_backtest.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'doorway.backtest'`

- [ ] **Step 3: Write the implementation**

```python
# src/doorway/backtest.py
"""Der Backtest und das Kill-Kriterium aus §14.2 der Spec.

Zwei Hürden, beide müssen halten:
  1. Von allen Urteilen "chancenlos" dürfen höchstens ein Prozent doch
     bewilligt worden sein.
  2. Jede ausgewiesene Klasse muss im Backtest innerhalb ihres angegebenen
     Intervalls liegen.

Bei Konflikt gewinnt Hürde 1: lieber gar keine Prozentzahl anzeigen, als
jemanden falsch abweisen.
"""

from dataclasses import dataclass, field
from typing import Iterable

from .basisrate import schaetzen
from .korpus import Entscheidung
from .regeln import REGELN, treffsicherheit
from .register import Registerzeile

GRENZE_FALSCHE_ABSAGEN = 0.01


@dataclass(frozen=True)
class Vorhersage:
    foerderelement: str
    jahr: int
    vorhergesagt: float
    tatsaechlich: float
    halbe_breite: float

    @property
    def getroffen(self) -> bool:
        return (
            self.vorhergesagt - self.halbe_breite
            <= self.tatsaechlich
            <= self.vorhergesagt + self.halbe_breite
        )


@dataclass(frozen=True)
class Bericht:
    absagen: list[tuple[str, int, int]] = field(default_factory=list)
    vorhersagen: list[Vorhersage] = field(default_factory=list)
    huerde_absagen_bestanden: bool = False
    huerde_kalibrierung_bestanden: bool = False

    @property
    def bestanden(self) -> bool:
        return self.huerde_absagen_bestanden and self.huerde_kalibrierung_bestanden


def kalibrierung(register: Iterable[Registerzeile]) -> list[Vorhersage]:
    """Sagt jedes Förderjahr aus den davor liegenden vorher."""
    register = list(register)
    elemente = {z.foerderelement for z in register if z.foerderelement}
    ergebnis: list[Vorhersage] = []
    for element in sorted(elemente):
        passend = [
            z
            for z in register
            if z.foerderelement == element and z.bewilligungsstelle is None and z.antraege
        ]
        nach_jahr = {z.foerderjahr: z for z in passend}
        for jahr in sorted(nach_jahr)[1:]:
            frueher = schaetzen(register, element, bis_jahr=jahr - 1)
            if frueher is None:
                continue
            heute = nach_jahr[jahr]
            ergebnis.append(
                Vorhersage(
                    foerderelement=element,
                    jahr=jahr,
                    vorhergesagt=frueher.quote,
                    tatsaechlich=heute.abgelehnt / heute.antraege,
                    halbe_breite=frueher.halbe_breite,
                )
            )
    return ergebnis


def absagen(entscheidungen: Iterable[Entscheidung]) -> list[tuple[str, int, int]]:
    """Je gemusterter Regel: Name, Treffer, davon faelschlich abgeraten."""
    entscheidungen = list(entscheidungen)
    return [
        (r.name, *treffsicherheit(r, entscheidungen))
        for r in REGELN
        if r.muster is not None
    ]


def pruefen(
    register: Iterable[Registerzeile], entscheidungen: Iterable[Entscheidung]
) -> Bericht:
    gemessen = absagen(entscheidungen)
    huerde1 = all(
        falsch / getroffen <= GRENZE_FALSCHE_ABSAGEN
        for _, getroffen, falsch in gemessen
        if getroffen
    )
    vorhersagen = kalibrierung(register)
    huerde2 = bool(vorhersagen) and all(v.getroffen for v in vorhersagen)
    return Bericht(gemessen, vorhersagen, huerde1, huerde2)


def als_text(bericht: Bericht) -> str:
    zeilen = ["KILL-KRITERIUM  (Spec Paragraph 14.2)", ""]

    zeilen.append("  Huerde 1  falsche Absagen")
    if not bericht.absagen:
        zeilen.append("    (keine messbare Regel)")
    for name, getroffen, falsch in bericht.absagen:
        quote = f"{falsch / getroffen:.1%}" if getroffen else "-"
        zeilen.append(f"    {name:<34} {falsch:>4}/{getroffen:<5} {quote:>7}")
    zeilen.append(
        f"    -> {'bestanden' if bericht.huerde_absagen_bestanden else 'GERISSEN'} "
        f"(Grenze {GRENZE_FALSCHE_ABSAGEN:.0%})"
    )
    zeilen.append("")

    zeilen.append("  Huerde 2  Kalibrierung")
    for v in bericht.vorhersagen:
        haken = "+" if v.getroffen else "X"
        zeilen.append(
            f"    {haken} {v.foerderelement:<16} {v.jahr}  "
            f"gesagt {v.vorhergesagt:>5.1%} +/- {v.halbe_breite:.1%}  "
            f"tatsaechlich {v.tatsaechlich:>5.1%}"
        )
    zeilen.append(
        f"    -> {'bestanden' if bericht.huerde_kalibrierung_bestanden else 'GERISSEN'}"
    )
    zeilen.append("")
    zeilen.append(
        "  ERGEBNIS: "
        + ("v1 darf live gehen." if bericht.bestanden else "v1 geht NICHT live.")
    )
    zeilen.append(
        "  Bei Konflikt gewinnt die Absage - lieber keine Zahl als eine falsche Abweisung."
    )
    return "\n".join(zeilen)
```

- [ ] **Step 4: Add the subcommand**

In `src/doorway/cli.py` nach `_prognose` einfügen:

```python
def _kill_kriterium(_args) -> int:
    from .backtest import als_text
    from .backtest import pruefen as backtest_pruefen

    bericht = backtest_pruefen(_register_bauen(), k.lesen(KORPUS))
    print(als_text(bericht))
    return 0 if bericht.bestanden else 1
```

Und in `main` bei den Unterbefehlen ergänzen, direkt nach dem `ernten`-Parser:

```python
    unter.add_parser(
        "kill-kriterium", help="Prueft beide Huerden aus Paragraph 14.2"
    ).set_defaults(fn=_kill_kriterium)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_backtest.py -v`
Expected: PASS, 9 Tests

- [ ] **Step 6: Run the whole suite and the real verdict**

```bash
python -m pytest -v
python -m doorway.cli kill-kriterium
```

Expected: Alle Tests grün. Der Befehl gibt beide Hürden mit Zahlen aus und endet mit „v1 darf live gehen." oder „v1 geht NICHT live." Der Rückgabewert ist 0 beziehungsweise 1.

**Das Ergebnis ist ein Befund, kein Fehler.** Reißt eine Hürde, ist das genau die Information, für die dieser Plan gebaut wurde — dann wird Teil 2 nicht begonnen, sondern Stufe 1 überarbeitet.

- [ ] **Step 7: Commit**

```bash
git add src/doorway/backtest.py src/doorway/cli.py tests/test_backtest.py
git commit -m "feat: Backtest und Kill-Kriterium aus Paragraph 14.2, beide Huerden messbar"
```

---

## Was dieser Plan bewusst nicht enthält

Diese Dinge stehen in der Spec, gehören aber in Teil 2 — nach dem Urteil des Kill-Kriteriums:

- **Der Spiegel** (§5.1): Lagebeschreibung in normaler Sprache. Hier wird das Förderelement als Parameter übergeben, statt aus einer Beschreibung erschlossen.
- **Das öffentliche Register** (§5.4): durchsuchbar und kostenlos im Netz. Hier entsteht es als CSV und JSON — der Rohstoff dafür, nicht die Oberfläche.
- **Die Nutzermeldungen mit Scoring Rule** (§8): Sie brauchen Nutzer, und Nutzer brauchen Teil 2.
- **Die Lückenschließung 2020 und 2022** über IFG-Anfragen (§7): ein Vorgang mit Behörden, kein Programmierschritt.
- **Die Quellen `vorl-17-2268` und `vorl-18-2806`** sind im Quellenregister erfasst, aber ohne Extraktor. Sie enthalten nur Ablehnungen ohne die zugehörigen Bewilligungen und können deshalb keine Quote tragen — sie sind Material für die Gründeverteilung in Teil 2.
