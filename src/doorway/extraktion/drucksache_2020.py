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
    """Letztes gueltiges Datum im Feld, sonst None.

    Bei zwei Antragsdaten ("15.11.2018/ 08.05.2019", Nr. 1417) zaehlt das
    letzte: das ist der Antrag, ueber den entschieden wurde. "13.09.20218"
    (Nr. 662) und "29.02.2019" (S. 114) sind keine Daten — nie schaetzen,
    das Feld bleibt leer, die Zeile bleibt.
    """
    treffer = re.findall(r"(?<!\d)\d{2}\.\d{2}\.\d{4}(?!\d)", text or "")
    if not treffer:
        return None
    try:
        return datetime.strptime(treffer[-1], "%d.%m.%Y").date().isoformat()
    except ValueError:
        return None


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
                # Nr. 644 traegt "Overath" in der Element-Spalte (Quellfehler).
                # Die Ablehnung ist echt; das Element bleibt "unbekannt".
                element = LANGFORM.get(feld["foerderelement"], "unbekannt")
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
