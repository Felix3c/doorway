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
