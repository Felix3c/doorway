"""Paragraph 10 der Spec als Test: Doorway darf keine Abrechnung werden.

Was nicht gespeichert ist, kann nicht blossstellen. Dieser Test schlaegt
fehl, sobald ein Antragstellername in den Korpus geraet.
"""

import json
from pathlib import Path

import pytest

from doorway.korpus import NAMENSMUSTER, lesen

KORPUS = Path("daten/korpus.jsonl")


def test_das_namensmuster_erkennt_die_ueblichen_rechtsformen():
    assert NAMENSMUSTER.search("Schuetzenbruderschaft St. Josef e.V. 1593")
    assert NAMENSMUSTER.search("Buergerstiftung Ahaus gGmbH")
    assert NAMENSMUSTER.search("Heimatverein Dolberg e. V.")


def test_das_namensmuster_schlaegt_bei_normalen_vorhabentexten_nicht_an():
    assert not NAMENSMUSTER.search("Restaurierung Schuetzenfahne")
    assert not NAMENSMUSTER.search("Anschaffung einer Projektionsanlage")
    assert not NAMENSMUSTER.search("Digitalisierung des Ortsarchivs")
    # Ein Vereinstyp im Titel ist kein Name; erst die Rechtsform macht ihn dazu.
    assert not NAMENSMUSTER.search("Ergaenzungsgebaeude fuer den Heimatverein")


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_im_geernteten_korpus_steht_kein_antragstellername():
    treffer = [
        (e.quelle_id, e.vorhabentext)
        for e in lesen(KORPUS)
        if e.vorhabentext and NAMENSMUSTER.search(e.vorhabentext)
    ]
    assert treffer == [], f"Klarnamen im Korpus: {treffer[:5]}"


@pytest.mark.skipif(not KORPUS.exists(), reason="Korpus noch nicht geerntet")
def test_keine_zeile_des_korpus_traegt_ein_unerwartetes_feld():
    erlaubt = {
        "programm",
        "foerderelement",
        "foerderjahr",
        "kommune",
        "bezirksregierung",
        "antragstellertyp",
        "vorhabentext",
        "betrag_euro",
        "antragsdatum",
        "entscheidungsdatum",
        "status",
        "ablehnungsgrund_roh",
        "quelle_id",
        "quelle_seite",
    }
    for zeile in KORPUS.read_text(encoding="utf-8").splitlines():
        assert set(json.loads(zeile)) == erlaubt
