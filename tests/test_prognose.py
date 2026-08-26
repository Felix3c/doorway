from doorway.prognose import beurteilen, panel
from doorway.register import Registerzeile


def r(jahr, bewilligt, abgelehnt, gruende=None):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement="Heimat-Scheck",
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende=gruende or {},
        herkunft="gezaehlt",
        quelle_id="vorl-18-5027",
        quelle_seite=15,
    )


REGISTER = [
    r(2018, 814, 469),
    r(2019, 996, 659),
    r(2021, 850, 275),
    r(2024, 550, 396),
    r(
        2025,
        596,
        330,
        {"entspricht nicht den Foerderkriterien": 277, "vereinsuebliche Ausstattung": 23},
    ),
]


def test_ein_trikotantrag_ist_chancenlos_und_bekommt_keine_prozentzahl():
    u = beurteilen(REGISTER, "Neue Trikots fuer den Schuetzenverein", "Heimat-Scheck")
    assert u.chancenlos is True
    assert [x.name for x in u.regeln] == ["vereinseigene Ausstattung"]


def test_ein_unauffaelliges_vorhaben_bekommt_eine_schaetzung():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert u.chancenlos is False
    assert u.schaetzung is not None
    assert 0.0 < u.schaetzung.quote < 1.0


def test_das_urteil_nennt_auch_die_bestandenen_pruefungen():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert set(u.bestanden) == {
        "vereinseigene Ausstattung",
        "fehlende Antragsberechtigung",
        "Mehrfachantrag im Foerderjahr",
    }


def test_das_panel_zeigt_die_ausschlusspruefung_auch_im_guten_fall():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    text = panel(u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None)
    assert "Ausschlusspruefung" in text
    assert "3 von 3 bestanden" in text


def test_das_panel_nennt_im_schlechten_fall_die_regel_statt_einer_zahl():
    u = beurteilen(REGISTER, "Neue Trikots", "Heimat-Scheck")
    text = panel(u, "Neue Trikots", "Heimat-Scheck", None)
    assert "Chance nahe null" in text
    assert "vereinseigene Ausstattung" in text
    assert "%" not in text.split("Woran es hier scheitert")[0]


def test_das_panel_traegt_immer_eine_belegzeile():
    for vorhaben in ("Neue Trikots", "Ortsarchiv digitalisieren"):
        u = beurteilen(REGISTER, vorhaben, "Heimat-Scheck")
        assert "Beleg" in panel(u, vorhaben, "Heimat-Scheck", None)


def test_das_panel_weist_die_unsicherheit_aus():
    u = beurteilen(REGISTER, "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert "+/-" in panel(u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None)


def test_ohne_registerdaten_gibt_es_keine_erfundene_zahl():
    u = beurteilen([], "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert u.schaetzung is None
    assert "keine belegten Zahlen" in panel(
        u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None
    )


def test_mit_weniger_als_drei_jahren_zeigt_das_panel_keine_zahl():
    """Paragraph 14.2, praezisiert am 26.08.2026: keine Prozentzahl ohne
    drei belegte Jahre. Das Register selbst bleibt sichtbar."""
    u = beurteilen(REGISTER[-2:], "Ortsarchiv digitalisieren", "Heimat-Scheck")
    assert u.schaetzung is None
    text = panel(u, "Ortsarchiv digitalisieren", "Heimat-Scheck", None)
    assert "%" not in text.split("Woran es hier scheitert")[0]
    assert "erst ab drei" in text
