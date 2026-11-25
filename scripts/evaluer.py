"""Compare un fichier de signaux à la vérité terrain du simulacre.

Rend traçable, pour chaque dépendance injectée, si elle a été trouvée ou manquée, et
pour chaque signal s'il correspond à une dépendance réelle ou à un faux positif.
Ce script n'existe que parce que les données sont fictives : en contexte réel, la
vérité terrain n'est connue qu'après coup, par la validation des tech leads et par les
dépendances ratées (voir scripts/faux_positifs.py).
"""
from __future__ import annotations

import argparse
from collections import Counter

import commun as c


def correspond(sig: dict, gt: dict) -> bool:
    if "paire" in gt:
        paire = set(gt["paire"])
        if sig["epique"] in paire:
            autres = paire - {sig["epique"]}
            cible_ok = sig["equipe_cible"] == gt["equipe_cible"] or any(
                c.lire_epique(c.RACINE / f"backlog/epics/{x}.md")["equipe"] == sig["equipe_cible"] for x in autres)
            if cible_ok:
                return True
    if sig["epique"] != gt["epique"] or sig["equipe_cible"] != gt["equipe_cible"]:
        return False
    if gt.get("exige_domaine") and gt["exige_domaine"] not in sig.get("domaines", []):
        return False
    return True


def evaluer(signaux: dict) -> dict:
    vt = c.lire_yaml("evaluation/verite-terrain.yml")
    gts = vt["dependances"]
    pieges = vt["pieges_faux_positifs"]
    res_sig = []
    for s in signaux["signaux"]:
        match = [g["id"] for g in gts if correspond(s, g)]
        piege = [p["id"] for p in pieges if p["epique"] == s["epique"] and p["equipe_cible"] == s["equipe_cible"]]
        res_sig.append({"id": s["id"], "confiance": s.get("confiance", "?"),
                        "verdict": "vrai" if match else "faux positif",
                        "correspond_a": match, "piege": piege})
    trouvees = {m for r in res_sig for m in r["correspond_a"]}
    manquees = [g for g in gts if g["id"] not in trouvees]
    fp = [r for r in res_sig if r["verdict"] == "faux positif"]
    par_conf = Counter()
    fp_conf = Counter()
    for r in res_sig:
        par_conf[r["confiance"]] += 1
        if r["verdict"] == "faux positif":
            fp_conf[r["confiance"]] += 1
    return {
        "source": signaux.get("source"), "semaine": signaux.get("semaine"),
        "nb_signaux": len(res_sig), "nb_faux_positifs": len(fp),
        "nb_dependances": len(gts), "nb_trouvees": len(trouvees), "manquees": [g["id"] for g in manquees],
        "signaux": res_sig,
        "calibration": {k: {"signaux": par_conf[k], "faux_positifs": fp_conf[k]} for k in ("haute", "moyenne", "basse")},
        "_gts": gts, "_manquees": manquees,
    }


def rapport_md(e: dict) -> str:
    taux = e["nb_faux_positifs"] / e["nb_signaux"] if e["nb_signaux"] else 0
    md = [
        f"# Évaluation contre la vérité terrain (source : {e['source']}, semaine {e['semaine']})", "",
        c.AVERTISSEMENT, "",
        f"- Dépendances injectées trouvées : **{e['nb_trouvees']} / {e['nb_dependances']}**",
        f"- Faux positifs : **{e['nb_faux_positifs']} / {e['nb_signaux']}** ({taux:.0%})",
        "", "## Signal par signal", "",
        c.tableau_md(["Signal", "Confiance", "Verdict", "Dépendance", "Piège"],
                     [[r["id"], r["confiance"], r["verdict"], ", ".join(r["correspond_a"]) or "—",
                       ", ".join(r["piege"]) or "—"] for r in e["signaux"]]),
        "", "## Dépendances manquées", "",
    ]
    md += [f"- {g['id']} : {g['epique']} → {g['equipe_cible']}. {g['note']}" for g in e["_manquees"]] or ["Aucune."]
    md += ["", "## Calibration de la confiance", "",
           "La confiance n'est utile que si les signaux « haute » sont rarement faux.", "",
           c.tableau_md(["Confiance", "Signaux", "Faux positifs"],
                        [[k, v["signaux"], v["faux_positifs"]] for k, v in e["calibration"].items()])]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("signaux", help="chemin du JSON de signaux (ex. reports/signaux-2026-S48-regles.json)")
    args = ap.parse_args()
    s = c.lire_json(args.signaux)
    e = evaluer(s)
    # Rangé sous evaluation/ : ce dossier est masqué aux agents (il révèle la vérité terrain).
    nom = f"evaluation/rapports/evaluation-{s['semaine']}-{s['source']}"
    c.ecrire_json(nom + ".json", {k: v for k, v in e.items() if not k.startswith("_")})
    c.ecrire(nom + ".md", rapport_md(e))
    print(rapport_md(e))


if __name__ == "__main__":
    main()
