from pathlib import Path

import pytest

from doorway.backtest import als_text, kalibrierung, pruefen
from doorway.korpus import Entscheidung
from doorway.register import Registerzeile

KORPUS = Path("daten/korpus.jsonl")


def r(jahr, bewilligt, abgelehnt):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende={},
        herkunft="gezaehlt",
        quelle_id="test",
        quelle_seite=1,
    )


BELEGT = [
    r(2018, 814, 469),
    r(2019, 996, 659),
    r(2021, 850, 275),
    r(2024, 550, 396),
    r(2025, 596, 330),
]


def e(status):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=2025,
        kommune=None,
        bezirksregierung=None,
        antragstellertyp=None,
        vorhabentext="Neue Trikots",
        betrag_euro=None,
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=None,
        quelle_id="test",
        quelle_seite=1,
    )


def test_das_erste_jahr_wird_nicht_vorhergesagt():
    assert 2018 not in [v.jahr for v in kalibrierung(BELEGT)]


def test_jedes_spaetere_jahr_wird_vorhergesagt():
    assert [v.jahr for v in kalibrierung(BELEGT)] == [2019, 2021, 2024, 2025]


def test_eine_vorhersage_gilt_als_getroffen_wenn_sie_im_intervall_liegt():
    for v in kalibrierung(BELEGT):
        assert v.getroffen == (
            v.vorhergesagt - v.halbe_breite
            <= v.tatsaechlich
            <= v.vorhergesagt + v.halbe_breite
        )


def test_der_bericht_nennt_beide_huerden():
    bericht = pruefen(BELEGT, [])
    assert hasattr(bericht, "huerde_absagen_bestanden")
    assert hasattr(bericht, "huerde_kalibrierung_bestanden")


def test_bestanden_ist_nur_wahr_wenn_beide_huerden_halten():
    bericht = pruefen(BELEGT, [])
    assert bericht.bestanden == (
        bericht.huerde_absagen_bestanden and bericht.huerde_kalibrierung_bestanden
    )


def test_eine_falsche_absage_ueber_ein_prozent_reisst_die_erste_huerde():
    treffer = [e("abgelehnt")] * 50 + [e("bewilligt")] * 5
    assert pruefen(BELEGT, treffer).huerde_absagen_bestanden is False


def test_wenige_falsche_absagen_unter_ein_prozent_reissen_nicht():
    treffer = [e("abgelehnt")] * 200 + [e("bewilligt")]
    assert pruefen(BELEGT, treffer).huerde_absagen_bestanden is True


def test_der_text_nennt_bei_konflikt_den_vorrang_der_absage():
    assert "Bei Konflikt gewinnt die Absage" in als_text(pruefen(BELEGT, []))


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_der_echte_lauf_erzeugt_einen_lesbaren_bericht():
    from doorway.cli import _register_bauen
    from doorway.korpus import lesen

    text = als_text(pruefen(_register_bauen(), lesen(KORPUS)))
    assert "Huerde 1" in text and "Huerde 2" in text
