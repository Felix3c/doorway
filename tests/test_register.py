import csv

from doorway.korpus import Entscheidung
from doorway.register import als_csv, messen, zaehlen, zusammenfuehren


def e(element="Heimat-Scheck", jahr=2025, status="bewilligt", grund=None, stelle=None):
    return Entscheidung(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        kommune="Ahlen",
        bezirksregierung=stelle,
        antragstellertyp=None,
        vorhabentext="Backhaus",
        betrag_euro="2000.00",
        antragsdatum=None,
        entscheidungsdatum=None,
        status=status,
        ablehnungsgrund_roh=grund,
        quelle_id="vorl-18-5027",
        quelle_seite=16,
    )


def test_zaehlen_bildet_eine_zeile_je_element_jahr_und_stelle():
    zeilen = zaehlen(
        [e(), e(status="abgelehnt", grund="vereinsintern"), e(element="Heimat-Preis")]
    )
    assert len(zeilen) == 2
    scheck = next(z for z in zeilen if z.foerderelement == "Heimat-Scheck")
    assert (scheck.antraege, scheck.bewilligt, scheck.abgelehnt) == (2, 1, 1)


def test_zaehlen_bildet_zusaetzlich_die_landesweite_summenzeile():
    zeilen = zaehlen([e(stelle="Koeln"), e(stelle="Koeln", status="abgelehnt", grund="x"), e(stelle="Muenster")])
    landesweit = next(z for z in zeilen if z.bewilligungsstelle is None)
    assert (landesweit.antraege, landesweit.bewilligt, landesweit.abgelehnt) == (3, 2, 1)
    assert {z.bewilligungsstelle for z in zeilen} == {None, "Koeln", "Muenster"}


def test_zaehlen_setzt_herkunft_auf_gezaehlt():
    assert zaehlen([e()])[0].herkunft == "gezaehlt"


def test_zaehlen_sammelt_die_ablehnungsgruende_mit_haeufigkeit():
    zeilen = zaehlen(
        [
            e(status="abgelehnt", grund="vereinsintern"),
            e(status="abgelehnt", grund="vereinsintern"),
            e(status="abgelehnt", grund="entspricht nicht den Foerderkriterien"),
        ]
    )
    assert zeilen[0].ablehnungsgruende == {
        "vereinsintern": 2,
        "entspricht nicht den Foerderkriterien": 1,
    }


def test_die_ablehnungsquote_wird_aus_den_antraegen_berechnet():
    zeile = zaehlen([e(), e(status="abgelehnt", grund="x")])[0]
    assert zeile.ablehnungsquote == 0.5


def test_messen_uebernimmt_ein_aggregat_als_gemessen():
    zeilen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 1125,
                "bewilligt": 850,
                "abgelehnt": 275,
                "foerdervolumen_euro": "1700000.00",
                "seite": 9,
            }
        ],
        foerderjahr=2021,
        quelle_id="vorl-17-6633",
        achse="foerderelement",
    )
    assert zeilen[0].herkunft == "gemessen"
    assert zeilen[0].bewilligungsstelle is None
    assert zeilen[0].bewilligt == 850


def test_messen_auf_der_stellen_achse_laesst_das_element_offen():
    zeilen = messen(
        [
            {
                "bewilligungsstelle": "Koeln",
                "bewilligt": 134,
                "abgelehnt": 87,
                "foerdervolumen_euro": "551769.00",
                "seite": 6,
            }
        ],
        foerderjahr=2024,
        quelle_id="vorl-18-3926",
        achse="bewilligungsstelle",
    )
    assert zeilen[0].foerderelement is None
    assert zeilen[0].bewilligungsstelle == "Koeln"
    assert zeilen[0].antraege == 221


def test_zusammenfuehren_behaelt_gemessen_wenn_beide_uebereinstimmen():
    gezaehlt = zaehlen([e(), e()])
    gemessen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 2,
                "bewilligt": 2,
                "abgelehnt": 0,
                "foerdervolumen_euro": None,
                "seite": 1,
            }
        ],
        foerderjahr=2025,
        quelle_id="vorl-18-5027",
        achse="foerderelement",
    )
    ergebnis = zusammenfuehren(gezaehlt, gemessen)
    assert len(ergebnis) == 1
    assert ergebnis[0].herkunft == "gemessen"
    assert ergebnis[0].konflikt is None


def test_zusammenfuehren_meldet_konflikt_und_behaelt_beide_werte():
    gezaehlt = zaehlen([e(), e()])
    gemessen = messen(
        [
            {
                "foerderelement": "Heimat-Scheck",
                "antraege": 3,
                "bewilligt": 3,
                "abgelehnt": 0,
                "foerdervolumen_euro": None,
                "seite": 1,
            }
        ],
        foerderjahr=2025,
        quelle_id="vorl-18-5027",
        achse="foerderelement",
    )
    zeile = zusammenfuehren(gezaehlt, gemessen)[0]
    assert zeile.herkunft == "konflikt"
    assert zeile.konflikt == {
        "gemessen": {"antraege": 3, "bewilligt": 3, "abgelehnt": 0},
        "gezaehlt": {"antraege": 2, "bewilligt": 2, "abgelehnt": 0},
    }


def test_keine_registerzeile_hat_eine_leere_herkunft():
    for z in zusammenfuehren(zaehlen([e()]), []):
        assert z.herkunft in ("gemessen", "gezaehlt", "konflikt")


def test_als_csv_schreibt_die_herkunft_in_eine_eigene_spalte(tmp_path):
    datei = tmp_path / "register.csv"
    als_csv(zaehlen([e()]), datei)
    with open(datei, encoding="utf-8", newline="") as f:
        kopf = next(csv.reader(f, delimiter=";"))
    assert "herkunft" in kopf
