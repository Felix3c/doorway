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
