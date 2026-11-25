"""Contrôle des signaux produits par l'IA et création des tickets de validation.

  python scripts/signaux.py valider reports/signaux-2026-S48-ia.json
      Vérifie le format. Code retour 1 si invalide : le workflow bascule alors sur les
      signaux par règles (mode dégradé automatique).

  python scripts/signaux.py tickets reports/signaux-2026-S48-ia.json [--dry-run]
      Ouvre un ticket GitHub par signal (via la CLI gh), avec des étiquettes de type,
      de confiance et d'équipe. Idempotent : un signal déjà ouvert pour le trimestre
      n'est pas recréé.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import commun as c

CONFIANCES = ("haute", "moyenne", "basse")
ETIQUETTES = {
    "signal-dependance": ("5319e7", "Signal de dépendance à valider par un tech lead"),
    "a-valider": ("fbca04", "En attente de validation humaine"),
    "validation:confirmee": ("0e8a16", "Dépendance confirmée par un tech lead"),
    "validation:ecartee": ("b60205", "Signal écarté par un tech lead (faux positif)"),
    "type:connaissance": ("c5def5", "Il faut quelqu'un qui connaît le domaine"),
    "type:capacite-charge": ("c5def5", "Équipe trop chargée ou présente mais pas disponible"),
    "type:sequence-coordination": ("c5def5", "Une autre équipe doit livrer avant"),
    "confiance:haute": ("1d76db", "Score de confiance haut (critères observables)"),
    "confiance:moyenne": ("5ea0e6", "Score de confiance moyen"),
    "confiance:basse": ("a7c7f0", "Score de confiance bas"),
    "source:ia": ("ededed", "Signal produit par l'agent IA"),
    "source:regles": ("ededed", "Signal produit par les règles (mode dégradé)"),
}


def erreurs_format(d: dict) -> list[str]:
    err = []
    for k in ("semaine", "trimestre", "source", "signaux"):
        if k not in d:
            err.append(f"clé manquante : {k}")
    eps = {e["id"] for e in c.epiques()}
    eqs = set(c.equipes())
    doms = set(c.domaines())
    for i, s in enumerate(d.get("signaux", [])):
        ou = f"signaux[{i}]"
        for k in ("id", "epique", "equipe_cible", "domaines", "types", "confiance", "criteres"):
            if k not in s:
                err.append(f"{ou} : clé manquante {k}")
        if s.get("epique") not in eps:
            err.append(f"{ou} : épique inconnue {s.get('epique')}")
        if s.get("equipe_cible") not in eqs:
            err.append(f"{ou} : équipe inconnue {s.get('equipe_cible')}")
        if not set(s.get("domaines", [])) <= doms:
            err.append(f"{ou} : domaine inconnu dans {s.get('domaines')}")
        if not s.get("types") or not set(s.get("types", [])) <= set(c.TYPES):
            err.append(f"{ou} : types invalides {s.get('types')}")
        if s.get("confiance") not in CONFIANCES:
            err.append(f"{ou} : confiance invalide {s.get('confiance')}")
    return err


def gh(*args: str, entree: str | None = None) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, input=entree).stdout


def corps_ticket(s: dict, d: dict) -> str:
    meta = {k: s.get(k) for k in ("id", "epique", "equipe_cible", "types", "confiance", "score")}
    meta |= {"source": d["source"], "trimestre": d["trimestre"], "semaine": d["semaine"]}
    lignes = [
        f"**Épique** : {s['epique']} ({s.get('titre_epique', '')}), équipe {s.get('equipe_source', '?')}",
        f"**Équipe cible** : {s['equipe_cible']} ; **domaines** : {', '.join(s['domaines'])}",
        f"**Types** : {', '.join(s['types'])} ; **confiance** : {s['confiance']}"
        + (f" (score {s['score']})" if "score" in s else ""),
        "", "**Critères observables**", *[f"- {x}" for x in s.get("criteres", [])],
    ]
    if s.get("preuves"):
        lignes += ["", "**Preuves citées**", *[f"- {x}" for x in s["preuves"]]]
    if s.get("justification"):
        lignes += ["", "**Analyse**", s["justification"]]
    if s.get("doute"):
        lignes += ["", f"**Où l'analyse doute** : {s['doute']}"]
    lignes += [
        "", "---",
        f"Tech lead de {s['equipe_cible']} (ou de {s.get('equipe_source', '?')}) : ajouter l'étiquette "
        "`validation:confirmee` ou `validation:ecartee`, avec un commentaire qui explique. "
        "La décision est enregistrée dans `validation/journal.csv`.",
        "", "_Simulacre, données fictives. Signal produit par "
        + ("l'agent IA" if d["source"] == "ia" else "les règles (mode dégradé)") + " : ce n'est pas une décision._",
        "", f"<!-- signal: {json.dumps(meta, ensure_ascii=False)} -->",
    ]
    return "\n".join(lignes)


def creer_tickets(d: dict, dry_run: bool) -> None:
    if not dry_run:
        for nom, (couleur, desc) in ETIQUETTES.items():
            gh("label", "create", nom, "--color", couleur, "--description", desc, "--force")
        gh("label", "create", f"trimestre:{d['trimestre']}", "--color", "bfdadc", "--force")
        existants = json.loads(gh("issue", "list", "--label", "signal-dependance", "--label",
                                  f"trimestre:{d['trimestre']}", "--state", "all", "--limit", "500",
                                  "--json", "title"))
        deja = {t["title"].split("]")[0].lstrip("[") for t in existants}
    else:
        deja = set()
    for s in d["signaux"]:
        if s["id"] in deja:
            print(f"déjà ouvert : {s['id']}")
            continue
        titre = f"[{s['id']}] {s['epique']} dépend de {s['equipe_cible']} ({', '.join(s['types'])})"
        etiquettes = ["signal-dependance", "a-valider", f"confiance:{s['confiance']}", f"source:{d['source']}",
                      f"trimestre:{d['trimestre']}", *[f"type:{t}" for t in s["types"]]]
        if dry_run:
            print(f"[dry-run] {titre}  {etiquettes}")
            continue
        args = ["issue", "create", "--title", titre, "--body-file", "-"]
        for e in etiquettes:
            args += ["--label", e]
        print(gh(*args, entree=corps_ticket(s, d)).strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["valider", "tickets"])
    ap.add_argument("fichier")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        d = c.lire_json(a.fichier)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Illisible : {e}", file=sys.stderr)
        return 1
    err = erreurs_format(d)
    if err:
        print("Format invalide :\n- " + "\n- ".join(err), file=sys.stderr)
        return 1
    if a.action == "valider":
        print(f"{a.fichier} : {len(d['signaux'])} signaux, format valide.")
        return 0
    creer_tickets(d, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
