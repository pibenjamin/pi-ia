"""Ratio capacité-charge par équipe pour le trimestre planifié.

capacité brute   = somme sur les sprints de (ETP nominal - absences - présents non disponibles)
                   x points par ETP et par sprint
taux de livraison = moyenne, sur l'historique, de features livrées / features programmées
facteur qualité   = 1 / (1 + coef x anomalies pondérées moyennes par release)
                   (anomalies rattachées à l'équipe qui a livré)
capacité effective = capacité brute x taux de livraison x facteur qualité
ratio             = charge (somme des tailles d'épiques du trimestre) / capacité effective

Aucune donnée individuelle : uniquement des agrégats par équipe.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import commun as c


def calculer(trimestre: str | None = None) -> dict:
    p = c.parametres()
    pc = p["capacite"]
    trimestre = trimestre or p["trimestre_planifie"]
    historique = set(p["trimestres_historique"])

    dispo = defaultdict(lambda: {"nominal": 0.0, "absences": 0.0, "non_dispo": 0.0})
    for l in c.lire_csv("capacity/availability.csv"):
        if not l["sprint"].startswith(trimestre):
            continue
        d = dispo[l["equipe"]]
        d["nominal"] += float(l["etp_nominal"])
        d["absences"] += float(l["absences_etp"])
        d["non_dispo"] += float(l["presents_non_disponibles_etp"])

    taux = defaultdict(list)
    for l in c.lire_csv("history/livraisons.csv"):
        if l["trimestre"] in historique:
            taux[l["equipe"]].append(int(l["features_livrees"]) / int(l["features_programmees"]))

    anomalies = defaultdict(list)
    for l in c.lire_csv("history/anomalies.csv"):
        if l["trimestre"] in historique:
            anomalies[l["equipe_livreuse"]].append(
                int(l["anomalies_bloquantes"]) * pc["poids_anomalie_bloquante"]
                + int(l["anomalies_mineures"]) * pc["poids_anomalie_mineure"]
            )

    charge = defaultdict(int)
    sans_equipe = []
    eqs = c.equipes()
    for e in c.epiques(trimestre):
        if e["equipe"] in eqs:
            charge[e["equipe"]] += int(e.get("taille_points", 0))
        else:
            sans_equipe.append({"epique": e["id"], "taille_points": e.get("taille_points", 0)})

    res = {}
    for eq in sorted(eqs):
        d = dispo[eq]
        etp_dispo = d["nominal"] - d["absences"] - d["non_dispo"]
        brute = etp_dispo * pc["points_par_etp_par_sprint"]
        t = sum(taux[eq]) / len(taux[eq]) if taux[eq] else 1.0
        a = sum(anomalies[eq]) / len(anomalies[eq]) if anomalies[eq] else 0.0
        q = 1 / (1 + pc["coef_anomalies"] * a)
        eff = brute * t * q
        ratio = charge[eq] / eff if eff else float("inf")
        part_nd = d["non_dispo"] / d["nominal"] if d["nominal"] else 0.0
        if ratio > pc["seuil_surcharge"]:
            etat = "surcharge"
        elif ratio >= pc["seuil_tension"]:
            etat = "tension"
        else:
            etat = "ok"
        res[eq] = {
            "etp_sprints_nominal": round(d["nominal"], 1),
            "etp_sprints_absences": round(d["absences"], 1),
            "etp_sprints_presents_non_disponibles": round(d["non_dispo"], 1),
            "part_presents_non_disponibles": round(part_nd, 2),
            "capacite_brute_points": round(brute, 1),
            "taux_livraison_historique": round(t, 2),
            "anomalies_ponderees_par_release": round(a, 2),
            "facteur_qualite": round(q, 2),
            "capacite_effective_points": round(eff, 1),
            "charge_points": charge[eq],
            "ratio_charge_capacite": round(ratio, 2),
            "etat": etat,
            "alerte_non_disponible": part_nd > pc["seuil_non_disponible"],
        }
    return {"trimestre": trimestre, "equipes": res, "epiques_sans_equipe": sans_equipe}


def rapport_md(r: dict) -> str:
    lignes = []
    for eq, v in r["equipes"].items():
        lignes.append([
            eq, v["capacite_brute_points"], v["taux_livraison_historique"], v["facteur_qualite"],
            v["capacite_effective_points"], v["charge_points"], v["ratio_charge_capacite"],
            v["etat"] + (" ; non dispo élevé" if v["alerte_non_disponible"] else ""),
            f'{v["part_presents_non_disponibles"]:.0%}',
        ])
    md = [
        f"# Capacité-charge {r['trimestre']} (calcul par règles)", "", c.AVERTISSEMENT, "",
        c.tableau_md(
            ["Équipe", "Capacité brute", "Taux livraison", "Facteur qualité", "Capacité effective",
             "Charge", "Ratio", "État", "Présents non dispo"],
            lignes,
        ),
        "",
        "Méthode : voir `scripts/capacite.py` et `skills/capacite/SKILL.md`. Unité : points.",
    ]
    if r["epiques_sans_equipe"]:
        md += ["", "Épiques sans équipe, non comptées dans la charge : "
               + ", ".join(f"{x['epique']} ({x['taille_points']} pts)" for x in r["epiques_sans_equipe"])]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trimestre")
    args = ap.parse_args()
    r = calculer(args.trimestre)
    c.ecrire_json(f"reports/capacite-{r['trimestre']}.json", r)
    c.ecrire(f"reports/capacite-{r['trimestre']}.md", rapport_md(r))
    print(rapport_md(r))


if __name__ == "__main__":
    main()
