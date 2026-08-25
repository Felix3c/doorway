"""Einstiegspunkt: doorway <befehl>."""

import argparse
import json
import sys
from pathlib import Path

from . import korpus as k
from . import register as reg
from .laden import laden, lock_pruefen, lock_schreiben
from .prognose import beurteilen, panel
from .quellen import QUELLEN

QUELLVERZEICHNIS = Path("daten/quellen")
LOCK = Path("daten/quellen.lock.json")
KORPUS = Path("daten/korpus.jsonl")
REGISTER_CSV = Path("daten/register.csv")
REGISTER_JSON = Path("daten/register.json")
GOLDEN = Path("golden")


def _laden(_args) -> int:
    for q in QUELLEN.values():
        print(q.id, laden(q, QUELLVERZEICHNIS))
    if LOCK.exists():
        abweichend = lock_pruefen(QUELLVERZEICHNIS, LOCK)
        if abweichend:
            print("Pruefsumme abweichend:", ", ".join(abweichend), file=sys.stderr)
            return 1
    else:
        lock_schreiben(QUELLVERZEICHNIS, LOCK)
    return 0


def _register_bauen() -> list[reg.Registerzeile]:
    gezaehlt = reg.zaehlen(k.lesen(KORPUS))
    gemessen = reg.messen(
        json.loads((GOLDEN / "vorl-17-6633.json").read_text(encoding="utf-8")),
        foerderjahr=2021,
        quelle_id="vorl-17-6633",
        achse="foerderelement",
    ) + reg.messen(
        json.loads((GOLDEN / "vorl-18-3926.json").read_text(encoding="utf-8")),
        foerderjahr=2024,
        quelle_id="vorl-18-3926",
        achse="bewilligungsstelle",
    )
    return reg.zusammenfuehren(gezaehlt, gemessen)


def _ernten(_args) -> int:
    alle = k.aus_anlage_2025(
        json.loads((GOLDEN / "vorl-18-5027.json").read_text(encoding="utf-8"))
    ) + k.aus_drucksache_2020(
        json.loads((GOLDEN / "drs-17-9738.json").read_text(encoding="utf-8"))
    )
    print(k.schreiben(alle, KORPUS), "Entscheidungen im Korpus")
    zeilen = _register_bauen()
    reg.als_csv(zeilen, REGISTER_CSV)
    reg.als_json(zeilen, REGISTER_JSON)
    konflikte = sum(1 for z in zeilen if z.herkunft == "konflikt")
    print(len(zeilen), "Registerzeilen,", konflikte, "davon mit Konflikt")
    return 0


def _prognose(args) -> int:
    urteil = beurteilen(
        _register_bauen(),
        args.vorhaben,
        args.element,
        bewilligungsstelle=args.stelle,
        antragstellertyp=args.typ,
        mehrfachantrag=args.mehrfachantrag,
    )
    print(panel(urteil, args.vorhaben, args.element, args.stelle))
    return 0


def _kill_kriterium(_args) -> int:
    from .backtest import als_text
    from .backtest import pruefen as backtest_pruefen

    bericht = backtest_pruefen(_register_bauen(), k.lesen(KORPUS))
    print(als_text(bericht))
    return 0 if bericht.bestanden else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="doorway")
    unter = p.add_subparsers(dest="befehl", required=True)

    unter.add_parser("laden", help="Quelldokumente holen und pruefen").set_defaults(fn=_laden)
    unter.add_parser("ernten", help="Korpus und Register neu bauen").set_defaults(fn=_ernten)
    unter.add_parser(
        "kill-kriterium", help="Prueft beide Huerden aus Paragraph 14.2"
    ).set_defaults(fn=_kill_kriterium)

    pr = unter.add_parser("prognose", help="Prognose fuer ein Vorhaben")
    pr.add_argument("vorhaben")
    pr.add_argument("--element", default="Heimat-Scheck")
    pr.add_argument("--stelle", default=None)
    pr.add_argument("--typ", default=None)
    pr.add_argument("--mehrfachantrag", action="store_true")
    pr.set_defaults(fn=_prognose)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
