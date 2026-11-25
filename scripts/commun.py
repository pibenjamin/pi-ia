"""Fonctions partagées par les scripts du simulacre.

Tous les scripts fonctionnent sans IA et sans GitHub : c'est la base du mode dégradé.
Dépendance unique : PyYAML.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
REPORTS = RACINE / "reports"

TYPES = ("connaissance", "capacite-charge", "sequence-coordination")


def lire_yaml(chemin: str | Path):
    with open(RACINE / chemin, encoding="utf-8") as f:
        return yaml.safe_load(f)


def lire_csv(chemin: str | Path) -> list[dict]:
    p = RACINE / chemin
    if not p.exists():
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ajouter_csv(chemin: str | Path, ligne: dict, entetes: list[str]) -> None:
    p = RACINE / chemin
    nouveau = not p.exists() or p.stat().st_size == 0
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=entetes)
        if nouveau:
            w.writeheader()
        w.writerow({k: ligne.get(k, "") for k in entetes})


def parametres() -> dict:
    return lire_yaml("config/parametres.yml")


def domaines() -> dict[str, dict]:
    return {d["id"]: d for d in lire_yaml("domains/domains.yml")["domaines"]}


def relations_apprises() -> list[dict]:
    return lire_yaml("domains/domains.yml").get("relations_apprises", []) or []


def equipes() -> dict[str, dict]:
    return {e["id"]: e for e in lire_yaml("teams/teams.yml")["equipes"]}


def features() -> dict[str, dict]:
    return {f["id"]: f for f in lire_yaml("history/features.yml")["features"]}


_FRONT = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def lire_epique(chemin: Path) -> dict:
    texte = chemin.read_text(encoding="utf-8")
    m = _FRONT.match(texte)
    if not m:
        raise ValueError(f"En-tête YAML absent : {chemin}")
    meta = yaml.safe_load(m.group(1))
    meta["corps"] = m.group(2)
    meta["fichier"] = str(chemin.relative_to(RACINE))
    meta["domaines"] = {str(k): int(v) for k, v in (meta.get("domaines") or {}).items()}
    return meta


def epiques(trimestre: str | None = None) -> list[dict]:
    res = [lire_epique(p) for p in sorted((RACINE / "backlog/epics").glob("*.md"))]
    if trimestre:
        res = [e for e in res if str(e.get("trimestre")) == trimestre]
    return res


def semaine_iso(jour: dt.date | None = None) -> str:
    jour = jour or dt.date.today()
    annee, semaine, _ = jour.isocalendar()
    return f"{annee}-S{semaine:02d}"


def trimestre_de(jour: dt.date) -> str:
    return f"{jour.year}-T{(jour.month - 1) // 3 + 1}"


def comparer_trimestres(a: str, b: str) -> int:
    """<0 si a avant b, 0 si égal, >0 si a après b. Format AAAA-TN."""
    ka = (int(a[:4]), int(a[-1]))
    kb = (int(b[:4]), int(b[-1]))
    return (ka > kb) - (ka < kb)


def ecrire(chemin: str | Path, contenu: str) -> Path:
    p = RACINE / chemin
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenu, encoding="utf-8")
    return p


def ecrire_json(chemin: str | Path, donnees) -> Path:
    return ecrire(chemin, json.dumps(donnees, ensure_ascii=False, indent=2) + "\n")


def chemin_entree(chemin: str | Path) -> Path:
    """Accepte un chemin relatif au dossier courant ou à la racine du dépôt."""
    p = Path(chemin)
    return p if p.is_absolute() or p.exists() else RACINE / chemin


def lire_json(chemin: str | Path):
    with open(chemin_entree(chemin), encoding="utf-8") as f:
        return json.load(f)


def tableau_md(entetes: list[str], lignes: list[list]) -> str:
    out = ["| " + " | ".join(entetes) + " |", "|" + "|".join("---" for _ in entetes) + "|"]
    for l in lignes:
        out.append("| " + " | ".join(str(c) for c in l) + " |")
    return "\n".join(out)


AVERTISSEMENT = (
    "> Simulacre : données entièrement fictives. Ce rapport illustre une cible, "
    "pas un retour d'expérience."
)
