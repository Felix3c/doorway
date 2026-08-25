import json
from pathlib import Path

import pytest

from doorway.extraktion.anlage_2025 import extrahieren
from doorway.laden import pfad
from doorway.quellen import quelle

PDF = pfad(quelle("vorl-18-5027"), Path("daten/quellen"))
GOLDEN = Path("golden/vorl-18-5027.json")

pytestmark = pytest.mark.skipif(
    not PDF.exists(), reason="Quelldokument fehlt — erst `doorway laden` ausfuehren"
)


@pytest.fixture(scope="module")
def gelesen():
    return extrahieren(PDF)


def test_die_anlage_enthaelt_1296_entscheidungen(gelesen):
    assert len(gelesen) == 1296


def test_945_bewilligungen_und_351_ablehnungen(gelesen):
    assert sum(1 for z in gelesen if z["status"] == "bewilligt") == 945
    assert sum(1 for z in gelesen if z["status"] == "abgelehnt") == 351


def test_jede_zeile_traegt_genau_einen_der_beiden_status(gelesen):
    assert {z["status"] for z in gelesen} == {"bewilligt", "abgelehnt"}


def test_die_foerderelemente_sind_die_fuenf_bekannten(gelesen):
    assert {z["foerderelement"] for z in gelesen} == {
        "Heimat-Scheck",
        "Heimat-Preis",
        "Heimat-Fonds",
        "Heimat-Werkstatt",
        "Heimat-Zeugnis",
    }


def test_der_heimat_scheck_hat_596_bewilligungen_und_330_ablehnungen(gelesen):
    scheck = [z for z in gelesen if z["foerderelement"] == "Heimat-Scheck"]
    assert sum(1 for z in scheck if z["status"] == "bewilligt") == 596
    assert sum(1 for z in scheck if z["status"] == "abgelehnt") == 330


def test_der_heimat_preis_wurde_kein_einziges_mal_abgelehnt(gelesen):
    preis = [z for z in gelesen if z["foerderelement"] == "Heimat-Preis"]
    assert sum(1 for z in preis if z["status"] == "abgelehnt") == 0


def test_kein_feld_traegt_einen_antragstellernamen(gelesen):
    assert all("foerdernehmende" not in z for z in gelesen)
    assert all("e.V." not in (z["vorhabentext"] or "") for z in gelesen)


def test_ein_vorhaben_mit_dem_wort_webseite_ueberlebt_den_kopfzeilenfilter(gelesen):
    """Der Filter darf nur den Zeilenanfang pruefen.

    Eine Pruefung auf "Seite" als Teilstring wuerde "Neugestaltung der
    Webseite" verschlucken und die Gesamtzahl still verfaelschen.
    """
    assert any("ebseite" in (z["vorhabentext"] or "") for z in gelesen)


def test_das_ergebnis_stimmt_mit_dem_golden_file_ueberein(gelesen):
    assert gelesen == json.loads(GOLDEN.read_text(encoding="utf-8"))
