// site/hinterlegen.mjs — reines Modul, kein DOM. Eingaben -> Datei im festgehalten-Format v1.
// Spec: docs/superpowers/specs/2026-09-05-doorway-teil-3-hinterlegung-design.md §3, §4, §6.

const UMLAUTE = { ä: "ae", ö: "oe", ü: "ue", ß: "ss" };

export function kurzBilden(text) {
  const k = String(text).toLowerCase()
    .replace(/[äöüß]/g, (c) => UMLAUTE[c])
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return k.slice(0, 20).replace(/-+$/g, "");
}

const zwei = (n) => String(n).padStart(2, "0");
export const isoDatum = (d) => `${d.getFullYear()}-${zwei(d.getMonth() + 1)}-${zwei(d.getDate())}`;

export function idBilden(institution, ordner, jetzt) {
  const kurz = ordner || kurzBilden(institution) || "hinterlegt";
  return `${kurz}-${jetzt.getFullYear()}-${zwei(jetzt.getMonth() + 1)}${zwei(jetzt.getDate())}${zwei(jetzt.getHours())}${zwei(jetzt.getMinutes())}`;
}
