"""Anonymisation des exports et contrôle d'absence de données personnelles.

  python scripts/anonymiser.py transformer EXPORT.csv SORTIE.csv --correspondances FICHIER.yml
      Transforme un export brut d'outil de suivi : supprime les colonnes qui désignent des
      personnes, remplace les noms d'équipes par leur identifiant (EQ-x) selon un fichier
      de correspondances qui ne doit jamais être versionné (voir .gitignore : entrees/).

  python scripts/anonymiser.py verifier
      Parcourt les données versionnées et échoue si elles contiennent une adresse
      électronique, une colonne nominative, ou un terme de la liste noire locale
      (entrees/liste-noire.txt, non versionnée). À lancer avant chaque commit.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys

import commun as c

MOTS_PERSONNELS = {"assigne", "assigné", "assignee", "rapporteur", "reporter", "auteur", "author", "createur",
                   "créateur", "creator", "nom", "name", "prenom", "prénom", "email", "courriel", "user",
                   "utilisateur", "owner", "responsable", "personne", "matricule"}


def colonne_personnelle(nom: str) -> bool:
    return any(m in MOTS_PERSONNELS for m in re.split(r"[^a-zà-ÿ]+", nom.lower()))
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOSSIERS_DONNEES = ["domains", "teams", "backlog", "capacity", "history", "flux", "releases",
                    "validation", "decisions", "reports"]
# Seule exception autorisée : les identifiants de comptes GitHub qui jouent un rôle.
EXCEPTIONS = {"gouvernance/roles.yml"}


def transformer(source: str, sortie: str, correspondances: str) -> None:
    corr = c.lire_yaml(correspondances) if correspondances else {}
    equipes = corr.get("equipes", {})
    with open(source, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    if not lignes:
        raise SystemExit("export vide")
    gardees = [k for k in lignes[0] if not colonne_personnelle(k)]
    retirees = [k for k in lignes[0] if k not in gardees]
    inconnues = set()
    with open(sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=gardees)
        w.writeheader()
        for l in lignes:
            l = {k: l[k] for k in gardees}
            for k in gardees:
                if k.lower().startswith(("equipe", "équipe", "team")):
                    v = l[k]
                    if v not in equipes:
                        inconnues.add(v)
                    l[k] = equipes.get(v, "EQ-INCONNUE")
                l[k] = RE_EMAIL.sub("[courriel retiré]", l[k])
            w.writerow(l)
    print(f"Colonnes retirées : {', '.join(retirees) or 'aucune'}")
    if inconnues:
        print(f"Équipes sans correspondance (remplacées par EQ-INCONNUE) : {len(inconnues)}", file=sys.stderr)


def verifier() -> int:
    liste_noire = []
    p = c.RACINE / "entrees/liste-noire.txt"
    if p.exists():
        liste_noire = [x.strip().lower() for x in p.read_text(encoding="utf-8").splitlines()
                       if x.strip() and not x.startswith("#")]
    problemes = []
    for dossier in DOSSIERS_DONNEES:
        for f in (c.RACINE / dossier).rglob("*"):
            if not f.is_file() or f.suffix not in (".md", ".yml", ".yaml", ".csv", ".json"):
                continue
            rel = str(f.relative_to(c.RACINE))
            if rel in EXCEPTIONS:
                continue
            texte = f.read_text(encoding="utf-8")
            for m in RE_EMAIL.finditer(texte):
                problemes.append(f"{rel} : adresse électronique « {m.group(0)} »")
            if f.suffix == ".csv":
                entete = texte.splitlines()[0] if texte else ""
                for col in entete.split(","):
                    if colonne_personnelle(col) and col not in ("par", "conseil_par", "approuve_par"):
                        problemes.append(f"{rel} : colonne nominative « {col} »")
            bas = texte.lower()
            for terme in liste_noire:
                if terme in bas:
                    problemes.append(f"{rel} : terme de la liste noire")
    if problemes:
        print("Données personnelles ou réelles possibles :\n- " + "\n- ".join(problemes), file=sys.stderr)
        return 1
    print(f"Contrôle d'anonymisation : rien à signaler ({len(liste_noire)} terme(s) en liste noire locale).")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="action", required=True)
    t = sub.add_parser("transformer")
    t.add_argument("source")
    t.add_argument("sortie")
    t.add_argument("--correspondances", default="")
    sub.add_parser("verifier")
    a = ap.parse_args()
    if a.action == "transformer":
        transformer(a.source, a.sortie, a.correspondances)
        return 0
    return verifier()


if __name__ == "__main__":
    sys.exit(main())
