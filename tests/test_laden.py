import hashlib

import pytest

from doorway.laden import laden, lock_pruefen, lock_schreiben, pfad, pruefsumme
from doorway.quellen import quelle

Q = quelle("vorl-18-5027")


def test_pruefsumme_ist_sha256_des_inhalts(tmp_path):
    datei = tmp_path / "x.pdf"
    datei.write_bytes(b"%PDF-1.7 test")
    assert pruefsumme(datei) == hashlib.sha256(b"%PDF-1.7 test").hexdigest()


def test_laden_holt_die_datei_nur_einmal(tmp_path):
    aufrufe = []

    def hole(url):
        aufrufe.append(url)
        return b"%PDF-1.7 inhalt"

    laden(Q, tmp_path, hole=hole)
    laden(Q, tmp_path, hole=hole)
    assert aufrufe == [Q.url]
    assert pfad(Q, tmp_path).read_bytes() == b"%PDF-1.7 inhalt"


def test_laden_lehnt_ab_was_kein_pdf_ist(tmp_path):
    with pytest.raises(ValueError, match="kein PDF"):
        laden(Q, tmp_path, hole=lambda url: b"<html>Fehlerseite</html>")


def test_lock_schreiben_und_pruefen_findet_keine_abweichung(tmp_path):
    laden(Q, tmp_path, hole=lambda url: b"%PDF-1.7 inhalt")
    lock = tmp_path / "quellen.lock.json"
    eintraege = lock_schreiben(tmp_path, lock)
    assert eintraege[Q.id] == pruefsumme(pfad(Q, tmp_path))
    assert lock_pruefen(tmp_path, lock) == []


def test_lock_pruefen_meldet_eine_veraenderte_datei(tmp_path):
    laden(Q, tmp_path, hole=lambda url: b"%PDF-1.7 inhalt")
    lock = tmp_path / "quellen.lock.json"
    lock_schreiben(tmp_path, lock)
    pfad(Q, tmp_path).write_bytes(b"%PDF-1.7 etwas anderes")
    assert lock_pruefen(tmp_path, lock) == [Q.id]
