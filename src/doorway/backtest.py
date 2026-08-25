"""Der Backtest und das Kill-Kriterium aus §14.2 der Spec.

Zwei Hürden, beide müssen halten:
  1. Von allen Urteilen "chancenlos" dürfen höchstens ein Prozent doch
     bewilligt worden sein.
  2. Jede ausgewiesene Klasse muss im Backtest innerhalb ihres angegebenen
     Intervalls liegen.

Bei Konflikt gewinnt Hürde 1: lieber gar keine Prozentzahl anzeigen, als
jemanden falsch abweisen.
"""

from dataclasses import dataclass, field
from typing import Iterable

from .basisrate import schaetzen
from .korpus import Entscheidung
from .regeln import REGELN, treffsicherheit
from .register import Registerzeile

GRENZE_FALSCHE_ABSAGEN = 0.01


@dataclass(frozen=True)
class Vorhersage:
    foerderelement: str
    jahr: int
    vorhergesagt: float
    tatsaechlich: float
    halbe_breite: float

    @property
    def getroffen(self) -> bool:
        return (
            self.vorhergesagt - self.halbe_breite
            <= self.tatsaechlich
            <= self.vorhergesagt + self.halbe_breite
        )


@dataclass(frozen=True)
class Bericht:
    absagen: list[tuple[str, int, int]] = field(default_factory=list)
    vorhersagen: list[Vorhersage] = field(default_factory=list)
    huerde_absagen_bestanden: bool = False
    huerde_kalibrierung_bestanden: bool = False

    @property
    def bestanden(self) -> bool:
        return self.huerde_absagen_bestanden and self.huerde_kalibrierung_bestanden


def kalibrierung(register: Iterable[Registerzeile]) -> list[Vorhersage]:
    """Sagt jedes Förderjahr aus den davor liegenden vorher."""
    register = list(register)
    elemente = {z.foerderelement for z in register if z.foerderelement}
    ergebnis: list[Vorhersage] = []
    for element in sorted(elemente):
        passend = [
            z
            for z in register
            if z.foerderelement == element and z.bewilligungsstelle is None and z.antraege
        ]
        nach_jahr = {z.foerderjahr: z for z in passend}
        for jahr in sorted(nach_jahr)[1:]:
            frueher = schaetzen(register, element, bis_jahr=jahr - 1)
            if frueher is None:
                continue
            heute = nach_jahr[jahr]
            ergebnis.append(
                Vorhersage(
                    foerderelement=element,
                    jahr=jahr,
                    vorhergesagt=frueher.quote,
                    tatsaechlich=heute.abgelehnt / heute.antraege,
                    halbe_breite=frueher.halbe_breite,
                )
            )
    return ergebnis


def absagen(entscheidungen: Iterable[Entscheidung]) -> list[tuple[str, int, int]]:
    """Je gemusterter Regel: Name, Treffer, davon faelschlich abgeraten."""
    entscheidungen = list(entscheidungen)
    return [
        (r.name, *treffsicherheit(r, entscheidungen))
        for r in REGELN
        if r.muster is not None
    ]


def pruefen(
    register: Iterable[Registerzeile], entscheidungen: Iterable[Entscheidung]
) -> Bericht:
    gemessen = absagen(entscheidungen)
    huerde1 = all(
        falsch / getroffen <= GRENZE_FALSCHE_ABSAGEN
        for _, getroffen, falsch in gemessen
        if getroffen
    )
    vorhersagen = kalibrierung(register)
    huerde2 = bool(vorhersagen) and all(v.getroffen for v in vorhersagen)
    return Bericht(gemessen, vorhersagen, huerde1, huerde2)


def als_text(bericht: Bericht) -> str:
    zeilen = ["KILL-KRITERIUM  (Spec Paragraph 14.2)", ""]

    zeilen.append("  Huerde 1  falsche Absagen")
    if not bericht.absagen:
        zeilen.append("    (keine messbare Regel)")
    for name, getroffen, falsch in bericht.absagen:
        quote = f"{falsch / getroffen:.1%}" if getroffen else "-"
        zeilen.append(f"    {name:<34} {falsch:>4}/{getroffen:<5} {quote:>7}")
    zeilen.append(
        f"    -> {'bestanden' if bericht.huerde_absagen_bestanden else 'GERISSEN'} "
        f"(Grenze {GRENZE_FALSCHE_ABSAGEN:.0%})"
    )
    zeilen.append("")

    zeilen.append("  Huerde 2  Kalibrierung")
    for v in bericht.vorhersagen:
        haken = "+" if v.getroffen else "X"
        zeilen.append(
            f"    {haken} {v.foerderelement:<16} {v.jahr}  "
            f"gesagt {v.vorhergesagt:>5.1%} +/- {v.halbe_breite:.1%}  "
            f"tatsaechlich {v.tatsaechlich:>5.1%}"
        )
    zeilen.append(
        f"    -> {'bestanden' if bericht.huerde_kalibrierung_bestanden else 'GERISSEN'}"
    )
    zeilen.append("")
    zeilen.append(
        "  ERGEBNIS: "
        + ("v1 darf live gehen." if bericht.bestanden else "v1 geht NICHT live.")
    )
    zeilen.append(
        "  Bei Konflikt gewinnt die Absage - lieber keine Zahl als eine falsche Abweisung."
    )
    return "\n".join(zeilen)
