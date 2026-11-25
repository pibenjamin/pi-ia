"""Tableau de synthèse : regroupe les dernières sorties des agents dans reports/SYNTHESE.md.

Choix du format : un fichier Markdown versionné, lisible directement sur GitHub et sans
outil supplémentaire ; il est aussi recopié dans le résumé du workflow d'orchestration.
Fonctionne sans IA : il ne lit que des fichiers.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import commun as c


def dernier(motif: str) -> Path | None:
    fichiers = sorted(c.REPORTS.glob(motif))
    return fichiers[-1] if fichiers else None


def signaux_courants() -> tuple[dict | None, Path | None]:
    """Signaux IA de la semaine la plus récente, sinon ceux des règles."""
    semaines = sorted({p.name.split("-", 1)[1].rsplit("-", 1)[0] for p in c.REPORTS.glob("signaux-*.json")})
    if not semaines:
        return None, None
    s = semaines[-1]
    for src in ("ia", "regles"):
        p = c.REPORTS / f"signaux-{s}-{src}.json"
        if p.exists():
            return c.lire_json(p), p
    return None, None


def construire() -> str:
    t = c.parametres()["trimestre_planifie"]
    md = [f"# Tableau de synthèse, planification {t}", "", c.AVERTISSEMENT, "",
          "Chaque ligne renvoie au rapport détaillé. Les décisions sont dans les journaux versionnés.", ""]

    sig, chemin = signaux_courants()
    journal = {l["signal"]: l for l in c.lire_csv("validation/journal.csv") if l["trimestre"] == t}
    md += ["## 1. Dépendances", ""]
    if sig:
        md.append(f"Source : **{'agent IA' if sig['source'] == 'ia' else 'règles (mode dégradé)'}**, "
                  f"semaine {sig['semaine']} ([JSON]({chemin.name})).")
        md.append("")
        md.append(c.tableau_md(
            ["Signal", "Types", "Confiance", "Validation tech lead"],
            [[s["id"], ", ".join(s["types"]), s["confiance"],
              (journal[s["id"]]["decision"] + " par " + journal[s["id"]]["role"]) if s["id"] in journal else "à valider"]
             for s in sig["signaux"]]))
        ev = c.RACINE / f"evaluation/rapports/evaluation-{sig['semaine']}-{sig['source']}.json"
        if ev.exists():
            e = c.lire_json(ev)
            md += ["", f"_Simulacre uniquement_ : contre la vérité terrain, {e['nb_trouvees']} / {e['nb_dependances']} "
                   f"dépendances injectées trouvées, {e['nb_faux_positifs']} faux positifs sur {e['nb_signaux']} signaux "
                   f"([évaluation](../evaluation/rapports/{ev.with_suffix('.md').name}))."]
    else:
        md.append("Aucune analyse disponible.")

    fp = c.REPORTS / f"faux-positifs-{t}.json"
    if fp.exists():
        r = c.lire_json(fp)
        taux = "—" if r["taux_faux_positifs"] is None else f"{r['taux_faux_positifs']:.0%}"
        md += ["", f"Faux positifs du trimestre : **{taux}** ({r['ecartes']} écartés sur {r['signaux_valides']} validés) ; "
               f"dépendances ratées : **{len(r['dependances_ratees'])}** ([détail](faux-positifs-{t}.md))."]

    md += ["", "## 2. Décisions du PM", ""]
    dec = [l for l in c.lire_csv("decisions/journal.csv") if l["trimestre"] == t]
    md.append(c.tableau_md(["Signal", "Plan retenu", "Conseil", "Approuvé par"],
                           [[l["signal"], l["plan"], l["conseil_role"], l["approuve_role"]] for l in dec])
              if dec else "Aucune décision enregistrée.")

    md += ["", "## 3. Capacité-charge", ""]
    cap = c.REPORTS / f"capacite-{t}.json"
    if cap.exists():
        r = c.lire_json(cap)
        md.append(c.tableau_md(["Équipe", "Ratio charge / capacité", "État", "Présents non dispo"],
                               [[eq, v["ratio_charge_capacite"], v["etat"], f"{v['part_presents_non_disponibles']:.0%}"]
                                for eq, v in r["equipes"].items()]))
        md.append(f"\n[Détail](capacite-{t}.md)")
    else:
        md.append("Non calculée.")

    md += ["", "## 4. Flux", ""]
    fl = dernier("flux-*.json")
    if fl:
        r = c.lire_json(fl)
        md += [f"Semaine {r['semaine']} : {len(r['alertes'])} alerte(s). [Détail]({fl.with_suffix('.md').name})", ""]
        md += [f"- {a}" for a in r["alertes"]]
    else:
        md.append("Non calculé.")

    md += ["", "## 5. Backlog", ""]
    bl = dernier("backlog-*-regles.json")
    if bl:
        r = c.lire_json(bl)
        md += [f"- {', '.join(f['epiques'])} : {f['motif']}" for f in r["faiblesses"]] or ["Aucune faiblesse."]

    md += ["", "## 6. Release", ""]
    rel = dernier("release-*-preuves.json")
    if rel:
        r = c.lire_json(rel)
        ko = [x["critere"] for x in r["criteres"] if not x["respecte"]]
        md.append(f"{r['release']} : proposition des règles **{r['proposition_regles']}**"
                  + (f" (critères non respectés : {', '.join(ko)})" if ko else "") + f". [Preuves]({rel.with_suffix('.md').name})")
        rj = [l for l in c.lire_csv("releases/journal.csv") if l["release"] == r["release"]]
        md.append(f"Décision humaine : **{rj[-1]['decision']}** par {rj[-1]['role']}." if rj else "Décision humaine : en attente.")
    else:
        md.append("Aucune release candidate.")
    return "\n".join(md) + "\n"


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    md = construire()
    c.ecrire("reports/SYNTHESE.md", md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(md)
    print(md)


if __name__ == "__main__":
    main()
