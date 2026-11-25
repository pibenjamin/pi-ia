---
name: analyse-dependances
description: Analyse hebdomadaire du backlog anonymisé pour signaler les dépendances entre équipes (connaissance, capacité-charge, séquence et coordination), avec un score de confiance fondé sur des critères observables. À utiliser pour produire reports/signaux-AAAA-SS-ia.json et reports/dependances-AAAA-SS.md.
---

# Analyse des dépendances

Lire d'abord `skills/principes-communs.md`.

## Entrées
- `backlog/epics/*.md` : une épique par fichier ; en-tête avec l'équipe, le trimestre, la
  taille et les **domaines cochés avec un degré de certitude** (0 à 100).
- `domains/domains.yml` : 12 domaines, l'équipe référente de chacun, ses composants, et les
  `relations_apprises` (liens entre domaines découverts après coup).
- `teams/teams.yml` : expertise de chaque équipe par domaine.
- `history/features.yml` : features exposées par les composants, avec leur statut
  (livree / planifiee + trimestre / non_planifiee).
- `history/dependances-confirmees.csv` : dépendances confirmées les trimestres précédents.
- `reports/capacite-<trimestre>.json` : état de charge par équipe.
- `reports/signaux-<semaine>-regles.json` et `reports/backlog-<semaine>-regles.json` :
  ce qu'ont produit les règles. C'est la référence à améliorer.

## Les trois types de dépendance
- `connaissance` : il faut quelqu'un qui connaît le domaine, et l'équipe de l'épique n'a
  pas cette expertise.
- `capacite-charge` : l'équipe cible est trop chargée (`etat` = surcharge), ou présente
  mais pas disponible sur le projet (`alerte_non_disponible`).
- `sequence-coordination` : une autre équipe doit livrer avant. Toujours vérifier : **la
  feature dont on dépend est-elle déjà implémentée ?** Si elle est `livree`, ce n'est pas
  une dépendance de séquence.

## Méthode
1. Partir des signaux des règles. Pour chacun, décider : garder, modifier (types,
   confiance) ou écarter, avec un motif.
2. Chercher ce que les règles ne voient pas : un besoin décrit dans le texte de l'épique
   alors que le domaine n'est pas coché (ou coché avec une faible certitude). Exemple
   type : une exigence réglementaire de conservation qui relève d'un domaine non coché.
3. Signaler les épiques communes ou doublons entre équipes.
4. Ne pas créer de signal pour une épique sans équipe : la mentionner dans `doute`.

## Barème de confiance (critères observables)
| Critère | Points |
|---|---|
| domaine coché à 100 % | +2 |
| domaine coché entre le seuil et 99 % | +1 |
| cite une feature de l'équipe cible non livrée | +2 |
| la feature citée est prévue après le trimestre de l'épique, ou non planifiée | +1 |
| cite une épique de l'équipe cible | +2 |
| ne cite que des features déjà livrées | -2 |
| lien entre ces domaines déjà confirmé ou appris | +1 |
| l'équipe de l'épique n'a pas d'expertise sur le domaine | +1 |
| équipe cible en surcharge ou trop de présents non disponibles | +1 |
| besoin explicite dans le texte sur un domaine non coché (critère propre à l'IA) | +1 |

Score >= 5 : `haute` ; 3 ou 4 : `moyenne` ; <= 2 : `basse`. Recopier les critères retenus
dans `criteres`. La confiance sera comparée chaque trimestre au taux de faux positifs.

## Sortie 1 : `reports/signaux-<semaine>-ia.json`
```json
{
  "semaine": "2026-S48", "trimestre": "2027-T1", "source": "ia",
  "signaux": [{
    "id": "DEP-EP-102-EQ-F", "epique": "EP-102", "titre_epique": "...",
    "equipe_source": "EQ-A", "equipe_cible": "EQ-F",
    "domaines": ["DOM-12"], "types": ["connaissance", "sequence-coordination"],
    "score": 5, "confiance": "haute",
    "criteres": ["domaine coché entre le seuil et 99 %", "..."],
    "preuves": ["FEAT-121 (planifiee 2027-T1)"],
    "justification": "2 ou 3 phrases.",
    "doute": "Ce qui manque pour trancher, ou chaîne vide."
  }],
  "ecartes": [{"epique": "EP-301", "equipe_cible": "EQ-E", "motif": "FEAT-092 déjà livrée"}]
}
```
Identifiant : `DEP-<epique>-<equipe_cible>`. Valeurs de `types` et `confiance` : exactement
celles ci-dessus. Le fichier est contrôlé par `scripts/signaux.py valider` ; s'il est
invalide, le workflow revient aux signaux des règles.

## Sortie 2 : `reports/dependances-<semaine>.md`
Un rapport lisible : tableau des signaux (id, équipes, types, confiance, doute), puis
« Écarts avec les règles » (ce qui a été ajouté, retiré ou requalifié, et pourquoi), puis
« Questions pour les tech leads ». Commencer par l'avertissement de simulacre.
