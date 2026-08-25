from doorway.tabellen import Wort, spalte, zeilen


def test_woerter_gleicher_hoehe_bilden_eine_zeile():
    w = [
        Wort(63, 100.0, "Attendorn"),
        Wort(179, 100.4, "Heimat-Preis"),
        Wort(840, 101.0, "5.000,00"),
    ]
    assert [[x.text for x in z] for z in zeilen(w)] == [
        ["Attendorn", "Heimat-Preis", "5.000,00"]
    ]


def test_zeilen_werden_nach_hoehe_sortiert_ausgegeben():
    w = [Wort(63, 200.0, "unten"), Wort(63, 100.0, "oben")]
    assert [z[0].text for z in zeilen(w)] == ["oben", "unten"]


def test_woerter_einer_zeile_werden_nach_x_sortiert():
    w = [Wort(840, 100.0, "rechts"), Wort(63, 100.0, "links")]
    assert [x.text for x in zeilen(w)[0]] == ["links", "rechts"]


def test_zu_weit_auseinander_liegende_hoehen_sind_zwei_zeilen():
    w = [Wort(63, 100.0, "eins"), Wort(63, 112.0, "zwei")]
    assert len(zeilen(w)) == 2


def test_spalte_fasst_die_woerter_eines_x_bereichs_zusammen():
    z = [
        Wort(63, 100.0, "Bad"),
        Wort(78, 100.0, "Berleburg"),
        Wort(179, 100.0, "Heimat-Scheck"),
    ]
    assert spalte(z, 50, 170) == "Bad Berleburg"
    assert spalte(z, 170, 260) == "Heimat-Scheck"


def test_spalte_ist_leer_wenn_der_bereich_kein_wort_enthaelt():
    z = [Wort(63, 100.0, "Bad")]
    assert spalte(z, 800, 900) == ""
