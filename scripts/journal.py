"""Enregistre une décision humaine dans un journal versionné (CSV).

Trois journaux, une ligne par décision, toujours rattachée à un rôle :
- validation/journal.csv : un tech lead confirme ou écarte un signal de dépendance ;
- decisions/journal.csv  : le PM retient un plan, sur conseil du coordinateur ;
- releases/journal.csv   : le responsable release prononce go / no-go.

Utilisé par les workflows et, en mode dégradé, directement à la main :
  python scripts/journal.py validation --signal DEP-EP-102-EQ-F --decision confirmee --par mon-compte
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

import commun as c

JOURNAUX = {
    "validation": ("validation/journal.csv",
                   ["date", "trimestre", "signal", "source", "confiance", "decision", "par", "role", "commentaire"]),
    "decision": ("decisions/journal.csv",
                 ["date", "trimestre", "signal", "plan", "justification", "conseil_par", "conseil_role",
                  "approuve_par", "approuve_role"]),
    "release": ("releases/journal.csv",
                ["date", "release", "decision", "conditions", "par", "role"]),
}


def role_de(compte: str) -> str:
    """Retrouve le rôle d'un compte GitHub dans gouvernance/roles.yml."""
    roles = c.lire_yaml("gouvernance/roles.yml")["roles"]
    compte = (compte or "").lower()
    if not compte or compte == "a-renseigner":
        return "hors-roles"
    trouves = [r for r, v in roles.items() if str(v.get("github", "")).lower() == compte]
    return "+".join(trouves) if trouves else "hors-roles"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="journal", required=True)
    v = sub.add_parser("validation")
    v.add_argument("--signal", required=True)
    v.add_argument("--decision", required=True, choices=["confirmee", "ecartee"])
    v.add_argument("--par", required=True, help="compte GitHub de la personne qui décide")
    v.add_argument("--source", default="")
    v.add_argument("--confiance", default="")
    v.add_argument("--commentaire", default="")
    d = sub.add_parser("decision")
    d.add_argument("--signal", required=True)
    d.add_argument("--plan", required=True)
    d.add_argument("--justification", default="")
    d.add_argument("--conseil-par", required=True)
    d.add_argument("--approuve-par", required=True)
    r = sub.add_parser("release")
    r.add_argument("--release", required=True)
    r.add_argument("--decision", required=True, choices=["go", "go-sous-conditions", "no-go"])
    r.add_argument("--conditions", default="")
    r.add_argument("--par", required=True)
    for s in (v, d, r):
        s.add_argument("--trimestre", default=c.parametres()["trimestre_planifie"])
        s.add_argument("--exiger-role", default="", help="préfixe de rôle exigé (ex. TL-, PM)")
    a = ap.parse_args(argv)

    chemin, entetes = JOURNAUX[a.journal]
    ligne = {"date": dt.date.today().isoformat(), "trimestre": a.trimestre}
    if a.journal == "validation":
        ligne |= {"signal": a.signal, "source": a.source, "confiance": a.confiance, "decision": a.decision,
                  "par": a.par, "role": role_de(a.par), "commentaire": a.commentaire}
        qui = ligne["role"]
    elif a.journal == "decision":
        ligne |= {"signal": a.signal, "plan": a.plan, "justification": a.justification,
                  "conseil_par": a.conseil_par, "conseil_role": role_de(a.conseil_par),
                  "approuve_par": a.approuve_par, "approuve_role": role_de(a.approuve_par)}
        qui = ligne["approuve_role"]
    else:
        ligne |= {"release": a.release, "decision": a.decision, "conditions": a.conditions,
                  "par": a.par, "role": role_de(a.par)}
        qui = ligne["role"]
    if a.exiger_role and not any(x.startswith(a.exiger_role) for x in qui.split("+")):
        print(f"Refusé : le rôle « {qui} » ne commence pas par « {a.exiger_role} ». "
              "Renseigner gouvernance/roles.yml.", file=sys.stderr)
        return 2
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"role={qui}\n")
    c.ajouter_csv(chemin, ligne, entetes)
    print(f"{chemin} : {ligne}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
