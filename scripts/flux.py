"""Indicateurs de flux par équipe : WIP, cycle time, tickets qui stagnent.

Entrée : flux/tickets.csv (export anonymisé : ticket, équipe, statut, dates).
Sortie : reports/flux-AAAA-SS.{md,json}. Écrit alerte=true|false dans $GITHUB_OUTPUT
si la variable existe, pour que le workflow n'appelle l'IA qu'en cas de dérive.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import statistics
from collections import defaultdict

import commun as c


def d(s: str) -> dt.date | None:
    return dt.date.fromisoformat(s) if s else None


def percentile(vals: list[int], q: float) -> float:
    if not vals:
        return 0
    v = sorted(vals)
    k = (len(v) - 1) * q
    i = int(k)
    return v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * (k - i)


def calculer(semaine: str | None = None) -> dict:
    p = c.parametres()["flux"]
    ref = d(str(p["date_reference"]))
    par_eq = defaultdict(lambda: {"wip": 0, "cycle": [], "stagnants": []})
    for t in c.lire_csv("flux/tickets.csv"):
        e = par_eq[t["equipe"]]
        if t["statut"] in ("en-cours", "bloque"):
            e["wip"] += 1
            age = (ref - d(t["date_derniere_transition"])).days
            if age >= p["seuil_stagnation_jours"] or t["statut"] == "bloque":
                e["stagnants"].append({"ticket": t["ticket"], "statut": t["statut"], "jours_sans_mouvement": age})
        elif t["statut"] == "termine":
            e["cycle"].append((d(t["date_fin"]) - d(t["date_debut"])).days)
    res, alertes = {}, []
    for eq in sorted(par_eq):
        e = par_eq[eq]
        r = {
            "wip": e["wip"], "limite_wip": p["limite_wip"],
            "cycle_time_median_jours": statistics.median(e["cycle"]) if e["cycle"] else None,
            "cycle_time_p85_jours": round(percentile(e["cycle"], 0.85), 1),
            "tickets_termines": len(e["cycle"]),
            "stagnants": e["stagnants"],
        }
        if e["wip"] > p["limite_wip"]:
            alertes.append(f"{eq} : WIP {e['wip']} au-dessus de la limite {p['limite_wip']}")
        for s in e["stagnants"]:
            alertes.append(f"{eq} : {s['ticket']} ({s['statut']}) sans mouvement depuis {s['jours_sans_mouvement']} j")
        res[eq] = r
    return {"semaine": semaine or c.semaine_iso(ref), "date_reference": str(ref), "equipes": res, "alertes": alertes}


def rapport_md(r: dict) -> str:
    md = [f"# Flux, semaine {r['semaine']} (calcul par règles)", "", c.AVERTISSEMENT, "",
          c.tableau_md(["Équipe", "WIP / limite", "Cycle time médian (j)", "Cycle time p85 (j)", "Tickets qui stagnent"],
                       [[eq, f"{v['wip']} / {v['limite_wip']}", v["cycle_time_median_jours"], v["cycle_time_p85_jours"],
                         len(v["stagnants"])] for eq, v in r["equipes"].items()]),
          "", "## Alertes", ""]
    md += [f"- {a}" for a in r["alertes"]] or ["Aucune."]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--semaine")
    args = ap.parse_args()
    r = calculer(args.semaine)
    c.ecrire_json(f"reports/flux-{r['semaine']}.json", r)
    c.ecrire(f"reports/flux-{r['semaine']}.md", rapport_md(r))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"alerte={'true' if r['alertes'] else 'false'}\nsemaine={r['semaine']}\n")
    print(rapport_md(r))


if __name__ == "__main__":
    main()
