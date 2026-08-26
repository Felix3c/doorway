import math

from doorway.basisrate import schaetzen
from doorway.register import Registerzeile


def r(jahr, bewilligt, abgelehnt, element="Heimat-Scheck", stelle=None):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        bewilligungsstelle=stelle,
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


def test_die_schaetzung_nimmt_das_juengste_belegte_jahr_als_punktwert():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.quote == 330 / 926
    assert s.grundlage_n == 926


def test_das_intervall_folgt_der_jahresschwankung_nicht_dem_stichprobenfehler():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    p, n = 330 / 926, 926
    stichprobe = 1.96 * math.sqrt(p * (1 - p) / n)
    assert s.halbe_breite > stichprobe * 3


def test_das_intervall_deckt_die_beobachtete_spannweite_weitgehend_ab():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.untergrenze < 0.244
    assert s.obergrenze > 0.419


def test_bei_nur_einem_jahr_bleibt_der_stichprobenfehler_uebrig():
    s = schaetzen([r(2025, 596, 330)], "Heimat-Scheck")
    p, n = 330 / 926, 926
    assert s.halbe_breite == 1.96 * math.sqrt(p * (1 - p) / n)


def test_bis_jahr_blendet_spaetere_jahre_aus_fuer_den_backtest():
    s = schaetzen(BELEGT, "Heimat-Scheck", bis_jahr=2021)
    assert s.quote == 275 / 1125
    assert 2024 not in s.jahre


def test_ein_element_ohne_daten_liefert_keine_schaetzung():
    assert schaetzen(BELEGT, "Heimat-Werkstatt") is None


def test_die_stelle_wird_beruecksichtigt_wenn_sie_angegeben_ist():
    mit_stelle = BELEGT + [r(2024, 134, 87, stelle="Koeln")]
    s = schaetzen(mit_stelle, "Heimat-Scheck", bewilligungsstelle="Koeln")
    assert s.quote == 87 / 221


def test_die_schaetzung_nennt_die_jahre_auf_denen_sie_beruht():
    assert schaetzen(BELEGT, "Heimat-Scheck").jahre == (2018, 2019, 2021, 2024, 2025)


def test_chance_ist_die_gegenwahrscheinlichkeit_der_quote():
    s = schaetzen(BELEGT, "Heimat-Scheck")
    assert s.chance == 1.0 - s.quote


ANDERE = [
    r(2018, 100, 60, element="Heimat-Zeugnis"),
    r(2019, 100, 55, element="Heimat-Zeugnis"),
    r(2021, 100, 17, element="Heimat-Zeugnis"),
    r(2018, 100, 21, element="Heimat-Fonds"),
    r(2019, 100, 26, element="Heimat-Fonds"),
    r(2021, 100, 6, element="Heimat-Fonds"),
]


def test_bei_weniger_als_drei_vorjahren_gilt_die_uebergreifende_schwankung_als_untergrenze():
    """Gemessen am 25.08.2026: Scheck 2019 wurde aus einem Vorjahr mit +/-2,6 %
    vorhergesagt und lag daneben. Ein Jahr kennt keine Schwankung; die Schwankung
    der anderen Elemente ist die ehrlichere Untergrenze."""
    zwei_jahre = [r(2018, 814, 469), r(2019, 820, 470)]  # eigene Schwankung ~0
    mit_umfeld = schaetzen(zwei_jahre + ANDERE, "Heimat-Scheck", bis_jahr=2019)
    allein = schaetzen(zwei_jahre, "Heimat-Scheck")
    assert mit_umfeld.halbe_breite > allein.halbe_breite
    assert mit_umfeld.quote == allein.quote


def test_ohne_vergleichsjahre_bleibt_nur_der_stichprobenfehler():
    """Im ersten Jahr aller Elemente kennt niemand eine Schwankung — dann wird
    keine erfunden."""
    s = schaetzen([r(2018, 814, 469)] + ANDERE, "Heimat-Scheck", bis_jahr=2018)
    assert s.halbe_breite == schaetzen([r(2018, 814, 469)], "Heimat-Scheck").halbe_breite


def test_ab_drei_vorjahren_zaehlt_die_eigene_schwankung():
    s_mit = schaetzen(BELEGT + ANDERE, "Heimat-Scheck")
    s_ohne = schaetzen(BELEGT, "Heimat-Scheck")
    assert s_mit.halbe_breite == s_ohne.halbe_breite
