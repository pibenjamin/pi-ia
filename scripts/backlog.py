"""Signaux de faiblesse du backlog, par règles (référence et mode dégradé).

- ownership flou : épique sans équipe connue ;
- trop grosse : taille supérieure à 60 % de la capacité effective de l'équipe ;
- manque d'informations : pas de critères d'acceptation, ou description de moins de 15 mots ;
- doublon potentiel / épique commune : deux épiques d'équipes différentes dont les profils
  de domaines cochés se ressemblent (similarité cosinus >= 0,75).
"""
from __future__ import annotations

import argparse
import math
import re

import capacite
import commun as c

SEUIL_SIMILARITE = 0.75
PART_MAX_CAPACITE = 0.60
MOTS_MIN = 15


def cosinus(a: dict, b: dict) -> float:
    num = sum(a[k] * b.get(k, 0) for k in a)
    den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return num / den if den else 0.0


def section(corps: str, titre: str) -> str:
    m = re.search(rf"^## {titre}\s*\n(.*?)(?=^## |\Z)", corps, re.S | re.M)
    return m.group(1).strip() if m else ""


def analyser(trimestre: str | None = None, semaine: str | None = None) -> dict:
    p = c.parametres()
    trimestre = trimestre or p["trimestre_planifie"]
    eqs = c.equipes()
    cap = capacite.calculer(trimestre)["equipes"]
    eps = c.epiques(trimestre)
    faiblesses = []
    for e in eps:
        if e["equipe"] not in eqs:
            faiblesses.append({"epiques": [e["id"]], "motif": "ownership-flou",
                               "detail": f"équipe « {e['equipe']} » inconnue de teams/teams.yml"})
            continue
        eff = cap[e["equipe"]]["capacite_effective_points"]
        if e["taille_points"] > PART_MAX_CAPACITE * eff:
            faiblesses.append({"epiques": [e["id"]], "motif": "trop-grosse",
                               "detail": f"{e['taille_points']} pts pour une capacité effective de {eff} pts "
                                         f"({e['taille_points'] / eff:.0%}) : à découper"})
    for e in eps:
        desc = section(e["corps"], "Description")
        crit = section(e["corps"], "Critères d'acceptation")
        manques = []
        if not crit:
            manques.append("pas de critères d'acceptation")
        if len(desc.split()) < MOTS_MIN:
            manques.append(f"description de {len(desc.split())} mots")
        if manques:
            faiblesses.append({"epiques": [e["id"]], "motif": "manque-informations", "detail": ", ".join(manques)})
    for i, a in enumerate(eps):
        for b in eps[i + 1:]:
            if a["equipe"] == b["equipe"]:
                continue
            s = cosinus(a["domaines"], b["domaines"])
            if s >= SEUIL_SIMILARITE:
                faiblesses.append({"epiques": [a["id"], b["id"]], "motif": "doublon-potentiel",
                                   "detail": f"profils de domaines similaires ({s:.2f}), équipes "
                                             f"{a['equipe']} et {b['equipe']} : épique commune ou doublon ?"})
    return {"semaine": semaine or c.semaine_iso(), "trimestre": trimestre, "source": "regles",
            "faiblesses": faiblesses}


def rapport_md(r: dict) -> str:
    md = [f"# Faiblesses du backlog {r['trimestre']}, semaine {r['semaine']} (source : {r['source']})", "",
          c.AVERTISSEMENT, "",
          c.tableau_md(["Épiques", "Motif", "Détail"],
                       [[", ".join(f["epiques"]), f["motif"], f["detail"]] for f in r["faiblesses"]]) if r["faiblesses"]
          else "Aucune faiblesse détectée.",
          "", "Ce sont des questions à poser aux équipes, pas des jugements."]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trimestre")
    ap.add_argument("--semaine")
    args = ap.parse_args()
    r = analyser(args.trimestre, args.semaine)
    c.ecrire_json(f"reports/backlog-{r['semaine']}-regles.json", r)
    c.ecrire(f"reports/backlog-{r['semaine']}-regles.md", rapport_md(r))
    print(rapport_md(r))


if __name__ == "__main__":
    main()
