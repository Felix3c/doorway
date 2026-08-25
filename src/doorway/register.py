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
    """Aggregiert Einzelentscheidungen zu Registerzeilen.

    Liegt eine Entscheidung mit Bezirksregierung vor, zaehlt sie doppelt:
    einmal fuer ihre Stelle und einmal fuer die landesweite Zeile
    (bewilligungsstelle=None, "ueber alle"). Ohne diese Summenzeile haetten
    die Jahre 2018/2019 keinen landesweiten Wert und die Kalibrierung wuerde
    2025 allein aus 2021 vorhersagen.
    """
    eimer: dict[tuple, list[Entscheidung]] = defaultdict(list)
    for e in entscheidungen:
        eimer[(e.programm, e.foerderelement, e.foerderjahr, e.bezirksregierung)].append(e)
        if e.bezirksregierung is not None:
            eimer[(e.programm, e.foerderelement, e.foerderjahr, None)].append(e)

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
