import json
from pathlib import Path

import pytest

from doorway.extraktion.aggregate import uebersicht_2021, uebersicht_2024
from doorway.laden import pfad
from doorway.quellen import quelle

PDF_2021 = pfad(quelle("vorl-17-6633"), Path("daten/quellen"))
PDF_2024 = pfad(quelle("vorl-18-3926"), Path("daten/quellen"))

pytestmark = pytest.mark.skipif(
    not (PDF_2021.exists() and PDF_2024.exists()),
    reason="Quelldokumente fehlen — erst `doorway laden` ausfuehren",
)


def test_uebersicht_2021_liefert_fuenf_elemente_und_die_summenzeile():
    assert [z["foerderelement"] for z in uebersicht_2021(PDF_2021)] == [
        "Heimat-Scheck",
        "Heimat-Preis",
        "Heimat-Fonds",
        "Heimat-Werkstatt",
        "Heimat-Zeugnis",
        None,
    ]


def test_uebersicht_2021_liest_den_heimat_scheck_korrekt():
    scheck = uebersicht_2021(PDF_2021)[0]
    assert (scheck["antraege"], scheck["bewilligt"], scheck["abgelehnt"]) == (
        1125,
        850,
        275,
    )
    assert scheck["foerdervolumen_euro"] == "1700000.00"


def test_uebersicht_2021_summenzeile_stimmt_mit_der_summe_der_elemente():
    zeilen = uebersicht_2021(PDF_2021)
    elemente, gesamt = zeilen[:-1], zeilen[-1]
    assert gesamt["antraege"] == sum(z["antraege"] for z in elemente) == 1513
    assert gesamt["bewilligt"] == sum(z["bewilligt"] for z in elemente) == 1219
    assert gesamt["abgelehnt"] == sum(z["abgelehnt"] for z in elemente) == 294


def test_uebersicht_2024_liefert_fuenf_bezirksregierungen_und_die_summenzeile():
    assert [z["bewilligungsstelle"] for z in uebersicht_2024(PDF_2024)] == [
        "Arnsberg",
        "Detmold",
        "Düsseldorf",
        "Köln",
        "Münster",
        None,
    ]


def test_uebersicht_2024_liest_koeln_und_muenster_korrekt():
    nach_stelle = {z["bewilligungsstelle"]: z for z in uebersicht_2024(PDF_2024)}
    assert (nach_stelle["Köln"]["bewilligt"], nach_stelle["Köln"]["abgelehnt"]) == (134, 87)
    assert (nach_stelle["Münster"]["bewilligt"], nach_stelle["Münster"]["abgelehnt"]) == (124, 36)


def test_uebersicht_2024_summenzeile_ist_883_bewilligt_und_427_abgelehnt():
    gesamt = uebersicht_2024(PDF_2024)[-1]
    assert gesamt["bewilligt"] == 883
    assert gesamt["abgelehnt"] == 427


def test_beide_uebersichten_stimmen_mit_ihren_golden_files_ueberein():
    assert uebersicht_2021(PDF_2021) == json.loads(
        Path("golden/vorl-17-6633.json").read_text(encoding="utf-8")
    )
    assert uebersicht_2024(PDF_2024) == json.loads(
        Path("golden/vorl-18-3926.json").read_text(encoding="utf-8")
    )
