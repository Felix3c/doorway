from pathlib import Path

import pytest

from doorway.genannt import (
    laden_genannte,
    normalisiert,
    seite_finden,
    vergleichen,
)
from doorway.laden import pfad
from doorway.quellen import quelle
from doorway.register import Registerzeile

GENANNTE = Path("golden/genannte-aggregate.json")


def r(element, jahr, bewilligt, abgelehnt):
    return Registerzeile(
        programm="Starke Heimat Nordrhein-Westfalen",
        foerderelement=element,
        foerderjahr=jahr,
        bewilligungsstelle=None,
        antraege=bewilligt + abgelehnt,
        bewilligt=bewilligt,
        abgelehnt=abgelehnt,
        foerdervolumen_euro=None,
        ablehnungsgruende={},
        herkunft="gezaehlt",
        quelle_id="vorl-18-5027",
        quelle_seite=15,
    )


def test_normalisiert_zieht_zeilenumbrueche_zu_einzelnen_leerzeichen_zusammen():
    assert normalisiert("konnten  598\n Schecks") == "konnten 598 Schecks"


def test_die_kuratierte_datei_enthaelt_nur_bekannte_quellen():
    for g in laden_genannte(GENANNTE):
        assert g.quelle_id in {"vorl-18-5027", "vorl-18-3926"}


def test_jeder_eintrag_traegt_ein_zitat_und_mindestens_eine_zahl():
    for g in laden_genannte(GENANNTE):
        assert g.zitat.strip()
        assert g.bewilligt is not None or g.abgelehnt is not None


def test_vergleichen_findet_den_belegten_widerspruch_von_zwei_und_eins():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderelement == "Heimat-Scheck"
                and g.foerderjahr == 2025]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 596, 330)])
    treffer = [e for e in ergebnis if e["befund"] == "konflikt"]
    assert len(treffer) == 1
    assert treffer[0]["differenz"] == {"bewilligt": 2, "abgelehnt": -1}


def test_vergleichen_meldet_uebereinstimmung_wenn_die_zahlen_gleich_sind():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderelement == "Heimat-Scheck"
                and g.foerderjahr == 2025]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 598, 329)])
    assert [e["befund"] for e in ergebnis] == ["stimmt"]


def test_vergleichen_meldet_fehlendes_gegenstueck_statt_es_zu_verschweigen():
    genannte = [g for g in laden_genannte(GENANNTE) if g.foerderjahr == 2024]
    ergebnis = vergleichen(genannte, [r("Heimat-Scheck", 2025, 596, 330)])
    assert [e["befund"] for e in ergebnis] == ["kein Gegenstueck"]


@pytest.mark.skipif(
    not pfad(quelle("vorl-18-5027"), Path("daten/quellen")).exists(),
    reason="Quelldokumente fehlen — erst `doorway laden` ausfuehren",
)
def test_jedes_zitat_steht_wirklich_im_quelldokument():
    fehlend = []
    for g in laden_genannte(GENANNTE):
        datei = pfad(quelle(g.quelle_id), Path("daten/quellen"))
        if seite_finden(datei, g.zitat) is None:
            fehlend.append((g.quelle_id, g.zitat))
    assert fehlend == [], f"Zitate nicht auffindbar: {fehlend}"
