# Mode dégradé manuel

Principe : **chaque étape peut se faire sans IA, et sans GitHub**. L'IA améliore une
référence produite par des règles ; elle ne la remplace pas.

## Niveau 1 : l'IA est coupée ou en panne

Rien à faire. Chaque workflow produit d'abord la version par règles, puis :

- si `AGENTS_IA_ACTIFS=false`, ou si aucun secret n'est configuré, l'agent n'est pas lancé ;
- si l'agent échoue ou produit un fichier invalide (`scripts/signaux.py valider`), le
  workflow garde la version par règles et l'écrit dans le résumé du run.

Pour le montrer : lancer un workflow en décochant l'entrée « ia ».

## Niveau 2 : GitHub Actions est indisponible

Tout se lance en local depuis une copie du dépôt (Python 3.10+, PyYAML) :

| Étape | Commande | Sortie |
|---|---|---|
| Contrôle d'anonymisation | `make verifier` | message ou liste des problèmes |
| Capacité-charge | `make capacite` | `reports/capacite-<trimestre>.md` |
| Dépendances | `make dependances SEMAINE=2026-S48` | `reports/dependances-<semaine>-regles.md` |
| Faiblesses du backlog | `make backlog SEMAINE=2026-S48` | `reports/backlog-<semaine>-regles.md` |
| Flux | `make flux` | `reports/flux-<semaine>.md` |
| Plans pour le PM | `make plans SIGNAL=DEP-EP-303-EQ-D` | `decisions/propositions/<signal>.md` |
| Preuves de release | `make release RELEASE=R-2027.1` | `reports/release-<release>-preuves.md` |
| Faux positifs | `make faux-positifs` | `reports/faux-positifs-<trimestre>.md` |
| Synthèse | `make synthese` | `reports/SYNTHESE.md` |

Les décisions s'enregistrent à la main, puis se commitent (le commit porte l'auteur) :

```bash
python scripts/journal.py validation --signal DEP-EP-502-EQ-C --decision ecartee --par <compte> --commentaire "FEAT-051 déjà livrée"
```

```bash
python scripts/journal.py decision --signal DEP-EP-303-EQ-D --plan "A. Attendre" --justification "FEAT-081 prévue en T2" --conseil-par <compte-coordinateur> --approuve-par <compte-pm>
```

```bash
python scripts/journal.py release --release R-2027.1 --decision go-sous-conditions --conditions "EP-602 sous feature flag désactivé" --par <compte>
```

Sans approbation par environnement GitHub, l'approbation du PM se fait par relecture de la
pull request qui ajoute la ligne au journal (relecteur obligatoire via `CODEOWNERS` ou
règle de branche).

## Niveau 3 : plus d'outil du tout

Le rapport `reports/dependances-*-regles.md` contient le barème de confiance ; les règles
sont décrites en tête de `scripts/dependances.py` et dans `skills/analyse-dependances/SKILL.md`.
Elles s'appliquent sur papier :

1. Pour chaque épique, lister les domaines cochés à 50 % ou plus dont l'équipe référente
   n'est pas l'équipe de l'épique.
2. Pour chacun : l'équipe a-t-elle l'expertise ? (sinon : connaissance). La feature citée
   est-elle livrée ? (sinon : séquence). L'équipe cible est-elle surchargée ou peu
   disponible ? (sinon : pas de capacité-charge).
3. Additionner les points du barème ; haute ≥ 5, moyenne 3-4, basse ≤ 2.
4. Faire valider par les tech leads, noter la décision dans un tableau à colonnes
   date / signal / décision / rôle.
5. En fin de trimestre, compter les signaux écartés (faux positifs) et les dépendances
   ratées ; ajouter chaque lien raté à la carte des domaines.

## Dépendances ratées

Quand une dépendance apparaît en cours de trimestre sans avoir été signalée, le
coordinateur l'ajoute dans `validation/dependances-ratees.yml` (exemple en commentaire du
fichier). `make faux-positifs` la compte et propose l'ajout du lien dans
`domains/domains.yml` (`relations_apprises`), à valider par un humain : la carte s'enrichit.
