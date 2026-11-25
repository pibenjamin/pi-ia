"""Plans proposés au PM pour une dépendance confirmée (version par règles, sans IA).

  python scripts/plans.py DEP-EP-303-EQ-D

Écrit decisions/propositions/<signal>.md avec 2 ou 3 plans parmi :
A. attendre le trimestre suivant (et prendre une feature secondaire),
B. réordonner dans le trimestre (l'équipe cible livre d'abord),
C. contrat d'interface avec mock et feature flag.
L'agent IA, s'il est actif, réécrit ce fichier en l'enrichissant ; le PM choisit.
"""
from __future__ import annotations

import argparse
import re
import sys

import capacite
import commun as c


def trouver_signal(signal_id: str) -> tuple[dict, dict] | None:
    for p in sorted(c.REPORTS.glob("signaux-*.json"), reverse=True):
        d = c.lire_json(p)
        for s in d["signaux"]:
            if s["id"] == signal_id:
                return s, d
    return None


def construire(signal_id: str) -> str:
    t = trouver_signal(signal_id)
    if not t:
        raise SystemExit(f"Signal introuvable dans reports/signaux-*.json : {signal_id}")
    s, d = t
    trimestre = d["trimestre"]
    eps = {e["id"]: e for e in c.epiques()}
    ep = eps[s["epique"]]
    feats = c.features()
    cites = [feats[f] for f in re.findall(r"FEAT-\d{3}", ep["corps"]) if f in feats]
    cibles = [f for f in cites if f["statut"] != "livree"]
    apres = [f for f in cibles if f["statut"] == "non_planifiee"
             or c.comparer_trimestres(str(f["trimestre"]), trimestre) > 0]
    cap = capacite.calculer(trimestre)["equipes"]
    src = cap[s["equipe_source"]]
    eff = src["capacite_effective_points"]
    ratio_sans = round((src["charge_points"] - ep["taille_points"]) / eff, 2)
    secondaires = [e for e in eps.values() if e["equipe"] == s["equipe_source"]
                   and str(e["trimestre"]) != trimestre and e["id"] != ep["id"]]

    plans = []
    plans.append(["A. Attendre", f"{ep['id']} passe au trimestre suivant"
                  + (f" ; feature secondaire possible : {secondaires[0]['id']}" if secondaires else " ; feature secondaire à choisir"),
                  f"ratio {s['equipe_source']} : {src['ratio_charge_capacite']} → {ratio_sans}",
                  "valeur décalée d'un trimestre"])
    if not apres:
        plans.append(["B. Réordonner", f"{s['equipe_cible']} livre "
                      + (", ".join(f["id"] for f in cibles) if cibles else "sa part") + f" en premier ; {ep['id']} démarre après",
                      f"ratio {s['equipe_cible']} : {cap[s['equipe_cible']]['ratio_charge_capacite']} (inchangé)",
                      "marge faible si l'équipe cible glisse"])
    plans.append(["C. Découpler", "contrat d'interface maintenant, mock côté "
                  f"{s['equipe_source']}, livraison sous feature flag désactivé",
                  "charge source + 10 à 20 % (mock, contrat)",
                  "le contrat peut changer quand l'équipe cible livre"])

    md = [f"# Propositions pour {signal_id}", "", c.AVERTISSEMENT, "",
          "_Version par règles (mode dégradé). Le choix revient au PM, sur conseil du coordinateur._", "",
          f"- Épique : {ep['id']} ({ep['titre']}), {s['equipe_source']}, {ep['taille_points']} points",
          f"- Dépend de : {s['equipe_cible']} ; types : {', '.join(s['types'])} ; confiance : {s['confiance']}",
          f"- Features attendues : " + (", ".join(f"{f['id']} ({f['statut']} {f.get('trimestre', '')})" for f in cibles) or "aucune citée"),
          "", c.tableau_md(["Plan", "Ce qui change", "Effet sur la charge", "Risque principal"], plans), ""]
    if apres:
        md.append(f"Plan B écarté : {', '.join(f['id'] for f in apres)} est prévue après {trimestre}.")
    md += ["", "## Où l'analyse doute", "",
           "- Le coût du mock (plan C) est une estimation forfaitaire, à confirmer par le tech lead.",
           "- Les règles ne connaissent pas la valeur métier : l'ordre de priorité reste au PM.", "",
           "## Pour décider", "",
           "Lancer le workflow « Décision du PM » avec ce signal et le plan retenu "
           "(approbation obligatoire du PM via l'environnement `decision-pm`), ou, en mode dégradé :",
           "", f"`python scripts/journal.py decision --signal {signal_id} --plan <A|B|C> "
           "--conseil-par <compte> --approuve-par <compte>`"]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("signal")
    a = ap.parse_args()
    md = construire(a.signal)
    c.ecrire(f"decisions/propositions/{a.signal}.md", md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
