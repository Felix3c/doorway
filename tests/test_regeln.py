from pathlib import Path

import pytest

from doorway.korpus import Entscheidung, lesen
from doorway.regeln import REGELN, pruefen, treffsicherheit

KORPUS = Path("daten/korpus.jsonl")


def e(text, status="abgelehnt"):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=2025,
        kommune="Ahlen",
        bezirksregierung=None,
        antragstellertyp=None,
        vorhabentext=text,
        betrag_euro=None,
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=None,
        quelle_id="vorl-18-5027",
        quelle_seite=1,
    )


def test_jede_regel_traegt_einen_beleg():
    for r in REGELN:
        assert r.beleg, f"Regel {r.name} ohne Beleg"
        assert "Drs" in r.beleg or "Vorl" in r.beleg


def test_trikots_loesen_die_ausstattungsregel_aus():
    assert [r.name for r in pruefen("Neue Trikots fuer die Jugendmannschaft")] == [
        "vereinseigene Ausstattung"
    ]


def test_eine_vereinsfahne_loest_die_ausstattungsregel_nicht_aus():
    """Gemessen: 41 von 44 Fahnenantraegen im Korpus wurden bewilligt."""
    assert pruefen("Restaurierung Vereinsfahne") == []


def test_eine_firma_ist_nicht_antragsberechtigt():
    assert [
        r.name for r in pruefen("Digitalisierung des Ortsarchivs", antragstellertyp="Firma")
    ] == ["fehlende Antragsberechtigung"]


def test_der_zweite_antrag_im_jahr_loest_die_mehrfachregel_aus():
    assert [
        r.name for r in pruefen("Digitalisierung des Ortsarchivs", mehrfachantrag=True)
    ] == ["Mehrfachantrag im Foerderjahr"]


def test_ein_unauffaelliges_vorhaben_loest_keine_regel_aus():
    assert pruefen("Digitalisierung des Ortsarchivs") == []


def test_ein_museumsprojekt_loest_keine_regel_aus():
    assert pruefen("Sonderausstellung zur Geschichte der Gesangvereine") == []


def test_treffsicherheit_zaehlt_treffer_und_fehltreffer():
    entscheidungen = [
        e("Neue Trikots"),
        e("Neue Trikots", status="bewilligt"),
        e("Digitalisierung"),
    ]
    regel = next(r for r in REGELN if r.name == "vereinseigene Ausstattung")
    assert treffsicherheit(regel, entscheidungen) == (2, 1)


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_keine_regel_reisst_die_ein_prozent_huerde():
    """Das Kill-Kriterium aus Paragraph 14.2, Huerde 1 — auf Regelebene."""
    entscheidungen = lesen(KORPUS)
    gerissen = []
    for r in REGELN:
        getroffen, faelschlich = treffsicherheit(r, entscheidungen)
        if getroffen == 0:
            continue
        quote = faelschlich / getroffen
        if quote > 0.01:
            gerissen.append(f"{r.name}: {faelschlich}/{getroffen} = {quote:.1%}")
    assert gerissen == [], "Regeln ueber der 1-Prozent-Huerde: " + "; ".join(gerissen)


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_jede_gemusterte_regel_findet_im_korpus_ueberhaupt_etwas():
    """Eine Regel, die nie feuert, ist Ballast und gehoert entfernt."""
    entscheidungen = lesen(KORPUS)
    stumm = [
        r.name
        for r in REGELN
        if r.muster is not None and treffsicherheit(r, entscheidungen)[0] == 0
    ]
    assert stumm == [], f"Regeln ohne einen einzigen Treffer: {stumm}"
