"""Teil 2, Abschnitt 1: der Export für die Seite.

Schreibt eine einzige, git-versionierte Datei `site/daten/panel.json`. Der
Browser rechnet nichts nach — er zeigt an, was Python hier entschieden hat.
Die Ausschlussregeln werden exportiert, nicht abgeschrieben: eine Quelle,
`regeln.py`. Beispiele je Regel erlauben dem Browser, sich selbst zu prüfen.
"""

import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import date
from pathlib import Path
from statistics import median

from . import korpus as k
from .basisrate import MINDESTJAHRE
from .prognose import beurteilen
from .quellen import QUELLEN
from .regeln import REGELN, pruefen

SCHWELLE_SPANNE = 0.20

ELEMENTE = ("Heimat-Scheck", "Heimat-Preis", "Heimat-Fonds", "Heimat-Werkstatt", "Heimat-Zeugnis")
SPIEGEL_TYPEN = ("Verein", "Initiative", "Stiftung", "Kirche", "Kommune", "Privatperson", "Firma")
BETRAGSKLASSEN = ("bis_2000", "bis_5000", "bis_50000", "mehr")

BEDINGUNGEN = {
    "fehlende Antragsberechtigung": "typ_firma",
    "Mehrfachantrag im Foerderjahr": "mehrfachantrag",
}

# Identisch mit den Faellen in tests/test_regeln.py; der Browser prueft sich damit.
BEISPIELE: dict[str, list[tuple[str, bool]]] = {
    "vereinseigene Ausstattung": [
        ("Neue Trikots fuer die Jugendmannschaft", True),
        ("Beschaffung neuer Uniformen", True),
        ("Restaurierung Vereinsfahne", False),
        ("Digitalisierung des Ortsarchivs", False),
        ("Sonderausstellung zur Geschichte der Gesangvereine", False),
    ],
}

ERLAUBTE_FELDER = {
    "register": (
        "programm", "foerderelement", "foerderjahr", "bewilligungsstelle", "antraege",
        "bewilligt", "abgelehnt", "foerdervolumen_euro", "ablehnungsgruende", "herkunft",
        "quelle_id", "quelle_seite", "konflikt",
    ),
    "schaetzungen": (
        "quote", "halbe_breite", "untergrenze", "obergrenze", "grundlage_n", "jahre",
        "belegte_jahre", "darstellung", "gruende", "beleg",
    ),
    "regeln": ("name", "beleg", "hinweis", "muster", "flags", "bedingung"),
    "beispiele": (),
    "elemente": ("bewilligt_mit_betrag", "median_betrag", "typen"),
    "vorschlag": (),
    "quellen": ("dokument", "url", "datum", "beschreibung"),
    "stand": ("datum", "korpus_commit", "quellen_lock"),
}

_JS_FREMD = re.compile(r"\(\?<[=!]|\(\?P<|\(\?[a-zA-Z]+\)|\\p\{|[+*?}]\+|\(\?>")


def js_kompatibel(muster: str) -> bool:
    """Wahr, wenn das Muster in Python und JavaScript gleich liest."""
    return _JS_FREMD.search(muster) is None


def regeln_block() -> list[dict]:
    block = []
    for r in REGELN:
        eintrag = {"name": r.name, "beleg": r.beleg, "hinweis": r.hinweis}
        if r.muster is not None:
            eintrag["muster"] = r.muster.pattern
            eintrag["flags"] = "i" if r.muster.flags & re.IGNORECASE else ""
        else:
            eintrag["bedingung"] = BEDINGUNGEN[r.name]
        block.append(eintrag)
    return block


def darstellung(halbe_breite: float, belegte_jahre: int) -> str:
    if belegte_jahre < MINDESTJAHRE:
        return "keine"
    return "punkt" if halbe_breite <= SCHWELLE_SPANNE else "spanne"


def vorschlag(betragsklasse: str, typ: str) -> str:
    """Elementvorschlag aus Betrag und Typ — belegt aus den Median-Betraegen
    und Typverteilungen des Korpus (siehe Spec Teil 2, Abschnitt 3)."""
    kommune = typ == "Kommune"
    if betragsklasse == "bis_2000":
        return "Heimat-Scheck"
    if betragsklasse == "bis_5000":
        return "Heimat-Preis" if kommune else "Heimat-Scheck"
    if betragsklasse == "bis_50000":
        return "Heimat-Fonds" if kommune else "Heimat-Werkstatt"
    return "Heimat-Zeugnis"


VORSCHLAG = {
    klasse: {typ: vorschlag(klasse, typ) for typ in SPIEGEL_TYPEN} for klasse in BETRAGSKLASSEN
}


def _beispiele_pruefen() -> None:
    for name, faelle in BEISPIELE.items():
        for text, erwartet in faelle:
            if (name in [r.name for r in pruefen(text)]) is not erwartet:
                raise ValueError(f"Beispiel widerspricht der Regel: {name!r} / {text!r}")


def _elemente_block(entscheidungen: list) -> dict:
    betraege = defaultdict(list)
    typen = defaultdict(Counter)
    for e in entscheidungen:
        if e.status == "bewilligt" and e.betrag_euro:
            betraege[e.foerderelement].append(float(e.betrag_euro))
        if e.antragstellertyp and e.antragstellertyp != "unbekannt":
            typen[e.foerderelement][e.antragstellertyp] += 1
    return {
        el: {
            "bewilligt_mit_betrag": len(betraege[el]),
            "median_betrag": round(median(betraege[el])) if betraege[el] else None,
            "typen": typen[el].most_common(3),
        }
        for el in ELEMENTE
    }


def _schaetzungen_block(register) -> dict:
    block = {}
    for el in ELEMENTE:
        u = beurteilen(register, "", el)
        s = u.schaetzung
        block[el] = {
            "quote": s.quote if s else None,
            "halbe_breite": s.halbe_breite if s else None,
            "untergrenze": s.untergrenze if s else None,
            "obergrenze": s.obergrenze if s else None,
            "grundlage_n": s.grundlage_n if s else None,
            "jahre": list(s.jahre) if s else [],
            "belegte_jahre": u.belegte_jahre,
            "darstellung": darstellung(s.halbe_breite if s else 0.0, u.belegte_jahre),
            "gruende": u.gruende,
            "beleg": u.beleg,
        }
    return block


def _korpus_commit(korpus: Path) -> str:
    ergebnis = subprocess.run(
        ["git", "log", "-1", "--format=%h", "--", str(korpus)],
        capture_output=True, text=True, check=False,
    )
    return ergebnis.stdout.strip() or "unversioniert"


def exportieren(ziel: Path, korpus: Path = Path("daten/korpus.jsonl"),
                lock: Path = Path("daten/quellen.lock.json")) -> dict:
    from .cli import _register_bauen  # spaeter Import: cli importiert export

    _beispiele_pruefen()
    entscheidungen = k.lesen(korpus)
    register = _register_bauen()
    daten = {
        "register": [asdict(z) for z in register],
        "schaetzungen": _schaetzungen_block(register),
        "regeln": regeln_block(),
        "beispiele": BEISPIELE,
        "elemente": _elemente_block(entscheidungen),
        "vorschlag": VORSCHLAG,
        "quellen": {
            q.id: {"dokument": q.dokument, "url": q.url, "datum": q.datum.isoformat(),
                   "beschreibung": q.beschreibung}
            for q in QUELLEN.values()
        },
        "stand": {
            "datum": date.today().isoformat(),
            "korpus_commit": _korpus_commit(korpus),
            "quellen_lock": json.loads(lock.read_text(encoding="utf-8")) if lock.exists() else {},
        },
    }
    Path(ziel).parent.mkdir(parents=True, exist_ok=True)
    Path(ziel).write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    return daten
