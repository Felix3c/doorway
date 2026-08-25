import json
from pathlib import Path

import pytest

from doorway.extraktion.drucksache_2020 import extrahieren
from doorway.laden import pfad
from doorway.quellen import quelle

PDF = pfad(quelle("drs-17-9738"), Path("daten/quellen"))
GOLDEN = Path("golden/drs-17-9738.json")

pytestmark = pytest.mark.skipif(
    not PDF.exists(), reason="Quelldokument fehlt — erst `doorway laden` ausfuehren"
)


@pytest.fixture(scope="module")
def gelesen():
    return extrahieren(PDF)


def test_die_anlage_enthaelt_3317_entscheidungen(gelesen):
    assert len(gelesen) == 3317


def test_2098_bewilligungen_und_1219_ablehnungen(gelesen):
    assert sum(1 for z in gelesen if z["status"] == "bewilligt") == 2098
    assert sum(1 for z in gelesen if z["status"] == "abgelehnt") == 1219


def test_antragsjahr_2018_hat_912_bewilligungen_und_508_ablehnungen(gelesen):
    j = [z for z in gelesen if (z["antragsdatum"] or "").startswith("2018")]
    assert sum(1 for z in j if z["status"] == "bewilligt") == 912
    assert sum(1 for z in j if z["status"] == "abgelehnt") == 508


def test_antragsjahr_2019_hat_1185_bewilligungen_und_708_ablehnungen(gelesen):
    j = [z for z in gelesen if (z["antragsdatum"] or "").startswith("2019")]
    assert sum(1 for z in j if z["status"] == "bewilligt") == 1185
    assert sum(1 for z in j if z["status"] == "abgelehnt") == 708


def test_die_foerderelemente_werden_auf_die_lange_form_normalisiert(gelesen):
    elemente = {z["foerderelement"] for z in gelesen}
    assert "Heimat-Scheck" in elemente
    assert "Scheck" not in elemente


def test_haeufigster_ablehnungsgrund_ist_der_sammelgrund(gelesen):
    gruende = [z["ablehnungsgrund_roh"] for z in gelesen if z["status"] == "abgelehnt"]
    assert sum(1 for g in gruende if g == "entspricht nicht den Förderkriterien") == 556


def test_die_fuenf_regierungsbezirke_kommen_alle_vor(gelesen):
    assert {"Arnsberg", "Detmold", "Düsseldorf", "Köln", "Münster"} <= {
        z["bezirksregierung"] for z in gelesen
    }


def test_das_ergebnis_stimmt_mit_dem_golden_file_ueberein(gelesen):
    assert gelesen == json.loads(GOLDEN.read_text(encoding="utf-8"))
