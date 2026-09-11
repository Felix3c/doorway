"""Die von site/hinterlegen.mjs erzeugte Datei muss der Generator von festgehalten
ohne Fehler lesen und prüfen (Spec Teil 3 §7.2)."""
import shutil
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("wettbuch")
from wettbuch import lesen, pruefen  # noqa: E402

WURZEL = Path(__file__).resolve().parents[1]
BUCH_MD = """---
titel: Hinterlegt
halter: Testhalter
kontakt: https://example.org
seit: 2026-09-05
lizenz: CC0
format: v1
sammelbuch: true
---
Test.
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")
def test_beispieldatei_besteht_generatorpruefung(tmp_path: Path):
    r = subprocess.run(["node", str(WURZEL / "site" / "hinterlegen.pruefung.mjs"), "--beispiel"],
                       capture_output=True, text=True, encoding="utf-8", check=True)
    datei = r.stdout
    assert datei.startswith("---\nid: ")
    ident = datei.splitlines()[1].split(": ", 1)[1]

    (tmp_path / "BUCH.md").write_text(BUCH_MD, encoding="utf-8")
    (tmp_path / "wetten").mkdir()
    (tmp_path / "wetten" / f"{ident}.md").write_text(datei, encoding="utf-8")

    buch = lesen.buch_lesen(tmp_path)
    fehler = pruefen.buch_pruefen(buch)

    assert fehler == [], [f"{f.datei}: {f.feld} — {f.text}" for f in fehler]
    w = buch["wetten"][0]
    assert w["herkunft"] == "hinterlegt"
    assert w["prognosen"][0]["wert"] == 1.0
