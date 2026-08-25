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


RECHTSFORM = re.compile(r"\be\.\s?V\.|\bgGmbH\b|\bGmbH\b", re.IGNORECASE)


def ohne_klarnamen(vorhabentext: str, foerdernehmende: str) -> str | None:
    """Entfernt den Namen der Fördernehmenden aus dem Vorhabentitel.

    In einigen Zeilen steht der Vereinsname im Titel selbst ("Chronik für den
    Musikverein X e.V."). Steht er wörtlich drin, wird er gestrichen; bleibt
    danach noch eine Rechtsform übrig, fällt der Titel ganz weg. Die
    Leitplanke §13.3 geht vor dem Text.
    """
    text = vorhabentext
    if foerdernehmende and foerdernehmende in text:
        text = text.replace(foerdernehmende, "").strip(" -:–,„“\"")
    if RECHTSFORM.search(text):
        return None
    return text or None


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
            # Die Statusspalte beginnt mit dem Euro-Zeichen des Betrags
            # ("€ bewilligt"), deshalb Teilstring statt Zeilenanfang.
            marke = spalte(zeile, *SPALTEN["status"]).lower()
            if grund or "abgelehnt" in marke:
                status = "abgelehnt"
            elif "bewilligt" in marke:
                status = "bewilligt"
            else:
                continue
            titel = spalte(zeile, *SPALTEN["vorhabentext"])
            name = spalte(zeile, *SPALTEN["_foerdernehmende"])
            ergebnis.append(
                {
                    "kommune": spalte(zeile, *SPALTEN["kommune"]) or None,
                    "foerderelement": element,
                    "vorhabentext": ohne_klarnamen(titel, name) if titel else None,
                    "betrag_euro": _betrag(spalte(zeile, *SPALTEN["betrag"])),
                    "status": status,
                    "ablehnungsgrund_roh": grund or None,
                    "seite": seite + 1,
                }
            )
    return ergebnis
