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
