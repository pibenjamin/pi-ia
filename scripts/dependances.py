"""Détection des dépendances par règles (référence et mode dégradé, sans IA).

Pour chaque épique du trimestre et chaque domaine coché au-dessus du seuil de certitude,
dont l'équipe référente n'est pas l'équipe de l'épique, on produit un signal candidat
(regroupé par couple épique / équipe cible) et on lui attribue :

- des types :
  * connaissance : l'équipe de l'épique n'a pas d'expertise sur le domaine ;
  * sequence-coordination : l'épique cite une feature non livrée ou une épique de
    l'équipe cible (il faut que l'autre équipe livre avant), ou rien ne permet de trancher ;
  * capacite-charge : l'équipe cible est en surcharge ou a trop de présents non disponibles.
- un score de confiance fondé sur des critères observables (voir CRITERES).

Un candidat est écarté si l'équipe a l'expertise et que toutes les features citées
chez l'équipe cible sont déjà livrées : la feature dont on dépend existe déjà.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict

import capacite
import commun as c

CRITERES = {
    "certitude_100": (2, "domaine coché à 100 %"),
    "certitude_50": (1, "domaine coché entre le seuil et 99 %"),
    "feature_non_livree": (2, "cite une feature de l'équipe cible non livrée"),
    "feature_apres_trimestre": (1, "la feature citée est prévue après le trimestre de l'épique, ou non planifiée"),
    "epique_citee": (2, "cite une épique de l'équipe cible"),
    "seulement_livrees": (-2, "ne cite que des features déjà livrées"),
    "lien_historique": (1, "lien entre ces domaines déjà confirmé ou appris"),
    "sans_expertise": (1, "l'équipe de l'épique n'a pas d'expertise sur le domaine"),
    "cible_chargee": (1, "équipe cible en surcharge ou trop de présents non disponibles"),
}

RE_FEAT = re.compile(r"FEAT-\d{3}")
RE_EP = re.compile(r"EP-\d{3}")


def niveau(score: int, p: dict) -> str:
    if score >= p["seuil_confiance_haute"]:
        return "haute"
    if score >= p["seuil_confiance_moyenne"]:
        return "moyenne"
    return "basse"


def analyser(trimestre: str | None = None, semaine: str | None = None) -> dict:
    p = c.parametres()
    pd = p["dependances"]
    trimestre = trimestre or p["trimestre_planifie"]
    semaine = semaine or c.semaine_iso()
    doms, eqs, feats = c.domaines(), c.equipes(), c.features()
    toutes = {e["id"]: e for e in c.epiques()}
    cap = capacite.calculer(trimestre)["equipes"]

    liens = set()
    for l in c.lire_csv("history/dependances-confirmees.csv"):
        liens.add(frozenset((l["domaine_source"], l["domaine_cible"])))
    for r in c.relations_apprises():
        liens.add(frozenset((r["de"], r["vers"])))

    signaux, ecartes = [], []
    for e in c.epiques(trimestre):
        src = e["equipe"]
        if src not in eqs:
            continue  # ownership flou : traité par l'agent backlogs
        cites_feat = [feats[f] for f in RE_FEAT.findall(e["corps"]) if f in feats]
        cites_ep = [toutes[x] for x in RE_EP.findall(e["corps"]) if x in toutes and x != e["id"]]

        par_cible = defaultdict(list)
        for d, cert in e["domaines"].items():
            if cert < pd["seuil_certitude"]:
                continue
            cible = doms[d]["equipe_referente"]
            if cible != src:
                par_cible[cible].append((d, cert))

        for cible, liste in sorted(par_cible.items()):
            comps = {cp for d, _ in liste for cp in doms[d]["composants"]}
            f_cible = [f for f in cites_feat if f["composant"] in comps]
            ep_cible = [x for x in cites_ep if x.get("equipe") == cible]
            sans_exp = [d for d, _ in liste if d not in eqs[src].get("expertise", {})]
            non_livrees = [f for f in f_cible if f["statut"] != "livree"]
            apres = [f for f in non_livrees
                     if f["statut"] == "non_planifiee"
                     or c.comparer_trimestres(str(f["trimestre"]), trimestre) > 0]
            charge = cap[cible]["etat"] == "surcharge" or cap[cible]["alerte_non_disponible"]

            if not sans_exp and f_cible and not non_livrees and not ep_cible:
                ecartes.append({
                    "epique": e["id"], "equipe_cible": cible, "domaines": [d for d, _ in liste],
                    "motif": "expertise présente et features citées déjà livrées : "
                             + ", ".join(f["id"] for f in f_cible),
                })
                continue

            types, crit = [], []
            if sans_exp:
                types.append("connaissance")
                crit.append("sans_expertise")
            if non_livrees or ep_cible or not sans_exp:
                types.append("sequence-coordination")
            if charge:
                types.append("capacite-charge")
                crit.append("cible_chargee")
            crit.append("certitude_100" if max(x for _, x in liste) == 100 else "certitude_50")
            if non_livrees:
                crit.append("feature_non_livree")
            if apres:
                crit.append("feature_apres_trimestre")
            if ep_cible:
                crit.append("epique_citee")
            if f_cible and not non_livrees:
                crit.append("seulement_livrees")
            if any(frozenset((d, d2)) in liens for d, _ in liste for d2 in e["domaines"] if d2 != d):
                crit.append("lien_historique")

            score = sum(CRITERES[k][0] for k in crit)
            doute = []
            if f_cible and not non_livrees:
                doute.append("Les features citées existent déjà : le besoin restant est peut-être nul.")
            if not sans_exp and not non_livrees and not ep_cible:
                doute.append("Aucune preuve dans le texte : signal fondé sur le seul cochage.")
            signaux.append({
                "id": f"DEP-{e['id']}-{cible}",
                "epique": e["id"],
                "titre_epique": e["titre"],
                "equipe_source": src,
                "equipe_cible": cible,
                "domaines": [d for d, _ in liste],
                "types": types,
                "score": score,
                "confiance": niveau(score, pd),
                "criteres": [CRITERES[k][1] for k in crit],
                "preuves": [f"{f['id']} ({f['libelle']}, {f['statut']} {f.get('trimestre', '')})".strip()
                            for f in f_cible] + [f"{x['id']} ({x['titre']}, {x['trimestre']})" for x in ep_cible],
                "doute": " ".join(doute),
            })

    signaux.sort(key=lambda s: (-s["score"], s["id"]))
    return {"semaine": semaine, "trimestre": trimestre, "source": "regles",
            "signaux": signaux, "ecartes": ecartes}


def rapport_md(r: dict) -> str:
    lignes = [[s["id"], s["equipe_source"] + " → " + s["equipe_cible"], ", ".join(s["domaines"]),
               ", ".join(s["types"]), f'{s["confiance"]} ({s["score"]})', s["doute"] or "—"]
              for s in r["signaux"]]
    md = [
        f"# Dépendances {r['trimestre']}, semaine {r['semaine']} (source : {r['source']})", "",
        c.AVERTISSEMENT, "",
        f"{len(r['signaux'])} signaux à valider par les tech leads. Aucun n'est une décision.", "",
        c.tableau_md(["Signal", "Équipes", "Domaines", "Types", "Confiance (score)", "Doute"], lignes),
        "", "## Détail des critères", "",
    ]
    for s in r["signaux"]:
        md.append(f"- **{s['id']}** ({s['titre_epique']}) : " + " ; ".join(s["criteres"])
                  + (f". Preuves : {', '.join(s['preuves'])}" if s.get("preuves") else ""))
    if r.get("ecartes"):
        md += ["", "## Candidats écartés", ""]
        md += [f"- {x['epique']} → {x['equipe_cible']} ({', '.join(x['domaines'])}) : {x['motif']}"
               for x in r["ecartes"]]
    md += ["", "Barème de confiance : "
           + " ; ".join(f"{v[1]} ({v[0]:+d})" for v in CRITERES.values()) + "."]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trimestre")
    ap.add_argument("--semaine")
    args = ap.parse_args()
    r = analyser(args.trimestre, args.semaine)
    c.ecrire_json(f"reports/signaux-{r['semaine']}-regles.json", r)
    c.ecrire(f"reports/dependances-{r['semaine']}-regles.md", rapport_md(r))
    print(rapport_md(r))


if __name__ == "__main__":
    main()
