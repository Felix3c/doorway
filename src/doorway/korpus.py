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

# Erkannt wird die Rechtsform, nicht das Wort "Verein": "Chronik fuer den
# Musikverein" ist ein Vorhaben, "Musikverein Velen e.V." ein Name.
NAMENSMUSTER = re.compile(r"\be\.\s?V\.|\bgGmbH\b|\bGmbH\b", re.IGNORECASE)

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
