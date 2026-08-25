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
