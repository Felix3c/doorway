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
