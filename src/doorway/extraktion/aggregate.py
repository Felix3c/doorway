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
