"""Mesure trimestrielle des faux positifs et des dépendances ratées.

- faux positif : signal écarté par un tech lead (validation/journal.csv) ;
- dépendance ratée : constatée en cours de trimestre sans avoir été signalée
  (validation/dependances-ratees.yml, renseigné par le coordinateur).

Chaque dépendance ratée produit une proposition d'enrichissement de la carte
(relations_apprises dans domains/domains.yml), à valider par un humain.
"""
from __future__ import annotations

import argparse
from collections import Counter

import commun as c


def calculer(trimestre: str | None = None) -> dict:
    trimestre = trimestre or c.parametres()["trimestre_planifie"]
    # dernière décision par signal (un tech lead peut revenir sur une décision)
    dernieres = {}
    for l in c.lire_csv("validation/journal.csv"):
        if l["trimestre"] == trimestre:
            dernieres[l["signal"]] = l
    dec = Counter(l["decision"] for l in dernieres.values())
    par_conf = Counter((l["confiance"] or "?", l["decision"]) for l in dernieres.values())
    ratees = [x for x in (c.lire_yaml("validation/dependances-ratees.yml") or {}).get("ratees", []) or []
              if str(x.get("trimestre")) == trimestre]
    connues = {frozenset((r["de"], r["vers"])) for r in c.relations_apprises()}
    propositions = [r for r in ratees
                    if r.get("domaine_source") and r.get("domaine_cible")
                    and frozenset((r["domaine_source"], r["domaine_cible"])) not in connues]
    valides = dec["confirmee"] + dec["ecartee"]
    return {
        "trimestre": trimestre,
        "signaux_valides": valides,
        "confirmes": dec["confirmee"],
        "ecartes": dec["ecartee"],
        "taux_faux_positifs": round(dec["ecartee"] / valides, 2) if valides else None,
        "par_confiance": {f"{k[0]}/{k[1]}": v for k, v in sorted(par_conf.items())},
        "dependances_ratees": ratees,
        "propositions_carte": propositions,
    }


def rapport_md(r: dict) -> str:
    taux = "—" if r["taux_faux_positifs"] is None else f"{r['taux_faux_positifs']:.0%}"
    md = [f"# Faux positifs et dépendances ratées, {r['trimestre']}", "", c.AVERTISSEMENT, "",
          f"- Signaux validés par les tech leads : {r['signaux_valides']}",
          f"- Confirmés : {r['confirmes']} ; écartés (faux positifs) : {r['ecartes']} ; taux : **{taux}**",
          f"- Dépendances ratées constatées : **{len(r['dependances_ratees'])}**", "",
          "## Par niveau de confiance", ""]
    md += [f"- {k} : {v}" for k, v in r["par_confiance"].items()] or ["Aucune validation enregistrée."]
    md += ["", "## Dépendances ratées", ""]
    md += [f"- {x['epique']} → {x['equipe_cible']} ({x.get('domaine_source', '?')} → {x.get('domaine_cible', '?')}) : "
           f"{x.get('constat', '')}" for x in r["dependances_ratees"]] or ["Aucune."]
    md += ["", "## Propositions d'enrichissement de la carte (à valider)", ""]
    md += [f"- Ajouter dans `domains/domains.yml`, `relations_apprises` : "
           f"`{{de: {x['domaine_source']}, vers: {x['domaine_cible']}, motif: \"{x.get('constat', '')}\", "
           f"appris: {r['trimestre']}}}`" for x in r["propositions_carte"]] or ["Aucune."]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trimestre")
    args = ap.parse_args()
    r = calculer(args.trimestre)
    c.ecrire_json(f"reports/faux-positifs-{r['trimestre']}.json", r)
    c.ecrire(f"reports/faux-positifs-{r['trimestre']}.md", rapport_md(r))
    print(rapport_md(r))


if __name__ == "__main__":
    main()
