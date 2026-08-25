from datetime import date

import pytest

from doorway.quellen import QUELLEN, quelle


def test_registry_enthaelt_die_sechs_belegten_dokumente():
    assert set(QUELLEN) == {
        "drs-17-9738",
        "vorl-17-2268",
        "vorl-17-6633",
        "vorl-18-2806",
        "vorl-18-3926",
        "vorl-18-5027",
    }


def test_jede_quelle_zeigt_auf_das_landtagsarchiv():
    for q in QUELLEN.values():
        assert q.url.startswith(
            "https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/"
        )
        assert q.url.endswith(".pdf")


def test_jedes_belegte_foerderjahr_hat_mindestens_eine_quelle():
    abgedeckt = {j for q in QUELLEN.values() for j in q.foerderjahre}
    assert {2018, 2019, 2021, 2023, 2024, 2025} <= abgedeckt


def test_die_luecken_2020_und_2022_sind_nicht_abgedeckt():
    abgedeckt = {j for q in QUELLEN.values() for j in q.foerderjahre}
    assert 2020 not in abgedeckt
    assert 2022 not in abgedeckt


def test_quelle_liefert_das_dokument_zum_bezeichner():
    q = quelle("vorl-18-5027")
    assert q.dokument == "MMV18-5027"
    assert q.datum == date(2026, 4, 21)
    assert q.foerderjahre == (2025,)
    assert q.art == "einzelfaelle"
    assert q.dateiname == "MMV18-5027.pdf"


def test_quelle_wirft_bei_unbekanntem_bezeichner():
    with pytest.raises(KeyError):
        quelle("gibt-es-nicht")
