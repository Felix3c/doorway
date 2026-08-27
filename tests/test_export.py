import json
import re
from pathlib import Path

import pytest

from doorway.export import (
    BEISPIELE,
    ERLAUBTE_FELDER,
    SCHWELLE_SPANNE,
    VORSCHLAG,
    darstellung,
    exportieren,
    js_kompatibel,
    regeln_block,
    vorschlag,
)
from doorway.regeln import REGELN, pruefen


def test_jede_regel_wird_mit_muster_oder_bedingung_exportiert():
    block = regeln_block()
    assert [r["name"] for r in block] == [r.name for r in REGELN]
    for r in block:
        assert r["beleg"] and r["hinweis"]
        assert ("muster" in r) != ("bedingung" in r)


def test_exportierte_muster_sind_javascript_kompatibel():
    for r in regeln_block():
        if "muster" in r:
            assert js_kompatibel(r["muster"]), r["muster"]


@pytest.mark.parametrize(
    "muster", [r"(?<=a)b", r"(?P<x>a)", r"(?i)a", r"\p{L}", r"a++", r"(?>a)"]
)
def test_js_kompatibel_lehnt_python_eigene_syntax_ab(muster):
    assert not js_kompatibel(muster)


def test_jedes_beispiel_stimmt_mit_der_python_regel_ueberein():
    for name, faelle in BEISPIELE.items():
        for text, erwartet in faelle:
            assert (name in [r.name for r in pruefen(text)]) is erwartet, (name, text)


def test_jede_gemusterte_regel_hat_beispiele_in_beide_richtungen():
    for r in REGELN:
        if r.muster is None:
            continue
        ergebnisse = {e for _, e in BEISPIELE[r.name]}
        assert ergebnisse == {True, False}, r.name


def test_darstellung_folgt_der_schwelle_und_paragraph_14_2():
    assert darstellung(halbe_breite=0.16, belegte_jahre=5) == "punkt"
    assert darstellung(halbe_breite=SCHWELLE_SPANNE, belegte_jahre=3) == "punkt"
    assert darstellung(halbe_breite=0.43, belegte_jahre=5) == "spanne"
    assert darstellung(halbe_breite=0.05, belegte_jahre=2) == "keine"


def test_vorschlag_folgt_betrag_und_typ():
    assert vorschlag("bis_2000", "Verein") == "Heimat-Scheck"
    assert vorschlag("bis_5000", "Kommune") == "Heimat-Preis"
    assert vorschlag("bis_5000", "Verein") == "Heimat-Scheck"
    assert vorschlag("bis_50000", "Kommune") == "Heimat-Fonds"
    assert vorschlag("bis_50000", "Verein") == "Heimat-Werkstatt"
    assert vorschlag("mehr", "Kommune") == "Heimat-Zeugnis"


def test_die_vorschlagstabelle_deckt_alle_kombinationen():
    typen = {"Verein", "Initiative", "Stiftung", "Kirche", "Kommune", "Privatperson", "Firma"}
    for klasse in ("bis_2000", "bis_5000", "bis_50000", "mehr"):
        for typ in typen:
            assert VORSCHLAG[klasse][typ] in {
                "Heimat-Scheck", "Heimat-Preis", "Heimat-Fonds", "Heimat-Werkstatt", "Heimat-Zeugnis",
            }


KORPUS = Path("daten/korpus.jsonl")


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_der_export_traegt_keine_felder_ausserhalb_der_liste(tmp_path):
    ziel = tmp_path / "panel.json"
    exportieren(ziel)
    daten = json.loads(ziel.read_text(encoding="utf-8"))
    assert set(daten) == set(ERLAUBTE_FELDER)
    for block, felder in ERLAUBTE_FELDER.items():
        if block in ("beispiele", "vorschlag"):
            continue
        eintraege = daten[block]
        if block == "stand":
            eintraege = [eintraege]
        elif isinstance(eintraege, dict):
            eintraege = list(eintraege.values())
        for e in eintraege:
            assert set(e) <= set(felder), (block, set(e) - set(felder))
    text = ziel.read_text(encoding="utf-8")
    for verboten in ('"kommune"', '"vorhabentext"', '"antragstellertyp"'):
        assert verboten not in text


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_der_export_hat_fuenf_schaetzungen_und_einen_stand(tmp_path):
    ziel = tmp_path / "panel.json"
    exportieren(ziel)
    daten = json.loads(ziel.read_text(encoding="utf-8"))
    assert set(daten["schaetzungen"]) == {
        "Heimat-Scheck", "Heimat-Preis", "Heimat-Fonds", "Heimat-Werkstatt", "Heimat-Zeugnis",
    }
    assert daten["schaetzungen"]["Heimat-Scheck"]["darstellung"] == "punkt"
    assert daten["schaetzungen"]["Heimat-Zeugnis"]["darstellung"] == "spanne"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", daten["stand"]["datum"])
    assert re.fullmatch(r"[0-9a-f]{7,40}", daten["stand"]["korpus_commit"])
