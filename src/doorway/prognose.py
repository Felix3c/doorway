"""Die Prognose: zweistufig gerechnet, einstufig angezeigt (§12 der Spec).

Die Regelprüfung entscheidet, welche Zeile das Gewicht trägt — sie erzeugt
keinen zweiten Bildschirm. Beide Fälle bekommen dasselbe Panel in derselben
Anordnung, damit das Auge nach dem zweiten Mal weiß, wo es hinschauen muss.
"""

from dataclasses import dataclass
from typing import Iterable

from .basisrate import Schaetzung, schaetzen
from .regeln import REGELN, Regel, pruefen
from .register import Registerzeile

BREITE = 70


@dataclass(frozen=True)
class Urteil:
    chancenlos: bool
    regeln: list[Regel]
    schaetzung: Schaetzung | None
    bestanden: list[str]
    gruende: dict[str, int]
    beleg: str


def beurteilen(
    register: Iterable[Registerzeile],
    vorhabentext: str,
    foerderelement: str,
    bewilligungsstelle: str | None = None,
    antragstellertyp: str | None = None,
    mehrfachantrag: bool = False,
) -> Urteil:
    register = list(register)
    getroffen = pruefen(vorhabentext, antragstellertyp, mehrfachantrag)
    namen = {r.name for r in getroffen}
    bestanden = [r.name for r in REGELN if r.name not in namen]

    schaetzung = schaetzen(register, foerderelement, bewilligungsstelle)
    mit_gruenden = [
        z
        for z in register
        if z.foerderelement == foerderelement
        and z.bewilligungsstelle == bewilligungsstelle
        and z.ablehnungsgruende
    ]
    gruende = mit_gruenden[-1].ablehnungsgruende if mit_gruenden else {}
    if mit_gruenden:
        beleg = f"{mit_gruenden[-1].quelle_id}, Seite {mit_gruenden[-1].quelle_seite}"
    elif schaetzung:
        beleg = schaetzung.quelle_id
    else:
        beleg = "keine Quelle"

    return Urteil(
        chancenlos=bool(getroffen),
        regeln=getroffen,
        schaetzung=schaetzung,
        bestanden=bestanden,
        gruende=gruende,
        beleg=beleg,
    )


def _zeile(text: str = "") -> str:
    return "| " + text[: BREITE - 4].ljust(BREITE - 4) + " |"


def panel(
    urteil: Urteil,
    vorhabentext: str,
    foerderelement: str,
    bewilligungsstelle: str | None,
) -> str:
    """Formt das Urteil als Textpanel — gleiche Form in beiden Fällen."""
    kopf = "CHANCENLOS" if urteil.chancenlos else "AUSSICHTSREICH"
    stelle = bewilligungsstelle or "landesweit"
    zeilen = [
        "+- " + kopf + " " + "-" * (BREITE - len(kopf) - 5) + "+",
        _zeile(vorhabentext),
        _zeile(f"{foerderelement} · {stelle}"),
        _zeile(),
    ]

    if urteil.chancenlos:
        r = urteil.regeln[0]
        zeilen += [
            _zeile("  X  Chance nahe null"),
            _zeile(f"     {r.name}"),
            _zeile(f"     {r.hinweis}"),
        ]
    elif urteil.schaetzung is None:
        zeilen += [_zeile("  ?  Fuer diese Kombination gibt es keine belegten Zahlen.")]
    else:
        s = urteil.schaetzung
        zeilen += [
            _zeile(f"  OK Chance rund {s.chance:.0%}      +/- {s.halbe_breite:.0%}"),
            _zeile(
                f"     Basis: {s.grundlage_n} Antraege, "
                f"Foerderjahre {s.jahre[0]}-{s.jahre[-1]}"
            ),
        ]

    zeilen += [
        _zeile(),
        _zeile(f"Ausschlusspruefung        {len(urteil.bestanden)} von {len(REGELN)} bestanden"),
    ]
    for r in REGELN:
        haken = "+" if r.name in urteil.bestanden else "X"
        zeilen.append(_zeile(f"  {haken} {r.name}"))

    if urteil.gruende:
        gesamt = sum(urteil.gruende.values())
        zeilen += [_zeile(), _zeile("Woran es hier scheitert")]
        for grund, anzahl in list(urteil.gruende.items())[:4]:
            marke = ""
            if urteil.chancenlos and urteil.regeln[0].name.lower()[:12] in grund.lower():
                marke = "  <- dein Fall"
            zeilen.append(_zeile(f"  {grund[:38]:<38} {anzahl / gesamt:>5.0%}{marke}"))

    zeilen += [_zeile(), _zeile(f"Beleg  {urteil.beleg}")]
    zeilen.append("+" + "-" * (BREITE - 2) + "+")
    return "\n".join(zeilen)
