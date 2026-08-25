"""Quelldokumente holen, lokal ablegen und gegen eine Lockdatei prüfen.

Die Dokumente sind unveränderlich. Ändert sich eine Prüfsumme, hat sich
entweder das Archiv geändert oder die lokale Datei ist beschädigt — in
beiden Fällen darf nicht stillschweigend weitergerechnet werden.
"""

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Callable

from .quellen import QUELLEN, Quelle

BLOCK = 1 << 20


def _hole_ueber_netz(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as antwort:
        return antwort.read()


def pfad(q: Quelle, verzeichnis: Path) -> Path:
    return Path(verzeichnis) / q.dateiname


def pruefsumme(datei: Path) -> str:
    h = hashlib.sha256()
    with open(datei, "rb") as f:
        while stueck := f.read(BLOCK):
            h.update(stueck)
    return h.hexdigest()


def laden(
    q: Quelle,
    verzeichnis: Path,
    hole: Callable[[str], bytes] = _hole_ueber_netz,
) -> Path:
    """Lädt das Dokument, falls es lokal noch nicht liegt. Gibt den Pfad zurück."""
    ziel = pfad(q, verzeichnis)
    if ziel.exists() and ziel.stat().st_size > 0:
        return ziel
    inhalt = hole(q.url)
    if not inhalt.startswith(b"%PDF"):
        raise ValueError(f"{q.id}: Antwort ist kein PDF ({inhalt[:40]!r})")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(inhalt)
    return ziel


def lock_schreiben(verzeichnis: Path, lockdatei: Path) -> dict[str, str]:
    """Schreibt die Prüfsummen aller lokal vorhandenen Quellen."""
    eintraege = {
        q.id: pruefsumme(pfad(q, verzeichnis))
        for q in QUELLEN.values()
        if pfad(q, verzeichnis).exists()
    }
    Path(lockdatei).parent.mkdir(parents=True, exist_ok=True)
    Path(lockdatei).write_text(
        json.dumps(eintraege, indent=1, sort_keys=True), encoding="utf-8"
    )
    return eintraege


def lock_pruefen(verzeichnis: Path, lockdatei: Path) -> list[str]:
    """Gibt die Bezeichner der Quellen zurück, deren Prüfsumme abweicht."""
    erwartet = json.loads(Path(lockdatei).read_text(encoding="utf-8"))
    abweichend = []
    for id, summe in erwartet.items():
        datei = pfad(QUELLEN[id], verzeichnis)
        if not datei.exists() or pruefsumme(datei) != summe:
            abweichend.append(id)
    return sorted(abweichend)
