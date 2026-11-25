"""Rassemble les preuves d'une release et évalue les critères go/no-go par règles.

Le résultat est un brouillon : la décision go/no-go reste humaine (environnement
GitHub « go-no-go » avec relecteur obligatoire, ou signature dans releases/journal.csv).
"""
from __future__ import annotations

import argparse

import commun as c


def evaluer(release: str) -> dict:
    r = c.lire_yaml(f"releases/{release}.yml")
    p = c.parametres()["release"]
    criteres = []

    def crit(nom, ok, detail):
        criteres.append({"critere": nom, "respecte": ok, "detail": detail})

    t = r["tests"]
    crit("tests automatisés", t["reussis"] == t["executes"], f"{t['reussis']} / {t['executes']} réussis")
    crit("couverture", t["couverture"] >= p["couverture_tests_min"],
         f"{t['couverture']:.0%} (minimum {p['couverture_tests_min']:.0%})")
    echecs = [s for s in r["non_regression"] if s["resultat"] != "ok"]
    crit("non-régression", not echecs,
         "toutes les suites passent" if not echecs else "; ".join(f"{s['suite']} : {s.get('detail', 'échec')}" for s in echecs))
    a = r["anomalies_ouvertes"]
    crit("anomalies bloquantes", a["bloquantes"] <= p["max_anomalies_bloquantes_ouvertes"],
         f"{a['bloquantes']} bloquantes, {a['mineures']} mineures ouvertes")
    suivies = {m["epique"] for m in r.get("plan_monitoring", [])}
    sans_plan = [x["epique"] for x in r["perimetre"] if x["epique"] not in suivies]
    crit("plan de monitoring", not sans_plan,
         "chaque épique a des indicateurs et un seuil de retour arrière" if not sans_plan
         else "sans plan : " + ", ".join(sans_plan))
    sans_flag = [x["epique"] for x in r["perimetre"] if not x.get("feature_flag")]
    crit("retour arrière", bool(r.get("retour_arriere")),
         r.get("retour_arriere", "absent") + (f" (sans feature flag : {', '.join(sans_flag)})" if sans_flag else ""))
    ko = [x for x in criteres if not x["respecte"]]
    proposition = "go" if not ko else ("no-go" if any(x["critere"] in ("anomalies bloquantes", "tests automatisés") for x in ko)
                                       else "go sous conditions")
    return {"release": release, "date_cible": str(r.get("date_cible")), "perimetre": r["perimetre"],
            "criteres": criteres, "proposition_regles": proposition}


def rapport_md(e: dict) -> str:
    md = [f"# Preuves de la release {e['release']} (calcul par règles)", "", c.AVERTISSEMENT, "",
          f"Proposition des règles : **{e['proposition_regles']}**. Brouillon : la décision reste humaine.", "",
          c.tableau_md(["Critère", "Respecté", "Détail"],
                       [[x["critere"], "oui" if x["respecte"] else "**non**", x["detail"]] for x in e["criteres"]]),
          "", "Périmètre : " + ", ".join(f"{x['epique']} ({x['equipe']})" for x in e["perimetre"])]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("release", help="ex. R-2027.1")
    args = ap.parse_args()
    e = evaluer(args.release)
    c.ecrire_json(f"reports/release-{args.release}-preuves.json", e)
    c.ecrire(f"reports/release-{args.release}-preuves.md", rapport_md(e))
    print(rapport_md(e))


if __name__ == "__main__":
    main()
