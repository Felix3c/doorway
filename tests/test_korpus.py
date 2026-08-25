from dataclasses import fields

import pytest

from doorway.korpus import Entscheidung, aus_anlage_2025, lesen, schreiben

ROH_2025 = [
    {
        "kommune": "Bad Berleburg",
        "foerderelement": "Heimat-Scheck",
        "vorhabentext": "Restaurierung Schuetzenfahne",
        "betrag_euro": "2000.00",
        "status": "abgelehnt",
        "ablehnungsgrund_roh": "vereinseigene Ausstattung",
        "seite": 21,
    },
    {
        "kommune": "Ahlen",
        "foerderelement": "Heimat-Scheck",
        "vorhabentext": "Backhaus",
        "betrag_euro": "5000.00",
        "status": "bewilligt",
        "ablehnungsgrund_roh": None,
        "seite": 16,
    },
]


def test_entscheidung_hat_kein_feld_fuer_den_antragstellernamen():
    namen = {f.name for f in fields(Entscheidung)}
    assert not namen & {"antragsteller", "foerdernehmende", "name", "verein"}


def test_aus_anlage_2025_setzt_programm_und_foerderjahr():
    e = aus_anlage_2025(ROH_2025)[0]
    assert e.programm == "Starke Heimat Nordrhein-Westfalen"
    assert e.foerderjahr == 2025
    assert e.quelle_id == "vorl-18-5027"


def test_aus_anlage_2025_uebernimmt_status_und_grund():
    abgelehnt, bewilligt = aus_anlage_2025(ROH_2025)
    assert abgelehnt.status == "abgelehnt"
    assert abgelehnt.ablehnungsgrund_roh == "vereinseigene Ausstattung"
    assert bewilligt.status == "bewilligt"
    assert bewilligt.ablehnungsgrund_roh is None


def test_aus_anlage_2025_laesst_unbekannte_felder_leer():
    e = aus_anlage_2025(ROH_2025)[0]
    assert e.bezirksregierung is None
    assert e.antragsdatum is None
    assert e.antragstellertyp is None


def test_schreiben_und_lesen_ergibt_dieselben_entscheidungen(tmp_path):
    entscheidungen = aus_anlage_2025(ROH_2025)
    datei = tmp_path / "korpus.jsonl"
    assert schreiben(entscheidungen, datei) == 2
    assert lesen(datei) == sorted(entscheidungen, key=Entscheidung.sortierschluessel)


def test_schreiben_sortiert_stabil_damit_diffs_lesbar_bleiben(tmp_path):
    datei = tmp_path / "korpus.jsonl"
    schreiben(aus_anlage_2025(ROH_2025), datei)
    erste = datei.read_text(encoding="utf-8")
    schreiben(aus_anlage_2025(list(reversed(ROH_2025))), datei)
    assert datei.read_text(encoding="utf-8") == erste


def test_ein_unbekannter_status_wird_abgelehnt():
    with pytest.raises(ValueError, match="Status"):
        aus_anlage_2025([{**ROH_2025[0], "status": "zurueckgezogen"}])
