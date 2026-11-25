---
name: propositions-plans
description: Pour une dépendance confirmée par un tech lead, proposer 2 ou 3 plans au PM (attendre le trimestre suivant, réordonner, contrat d'interface avec mock et feature flag), avec impacts, risques et doutes. À utiliser pour écrire decisions/propositions/<signal>.md.
---

# Propositions de plans

Lire d'abord `skills/principes-communs.md`. Le PM choisit, sur conseil du coordinateur.

## Entrées
Le signal confirmé (fichier `reports/signaux-*.json` le plus récent, et le texte du ticket
fourni dans le prompt), l'épique et l'épique dont elle dépend (`backlog/epics/`),
`history/features.yml`, `reports/capacite-<trimestre>.json`.

## Plans possibles (en proposer 2 ou 3, pas plus)
- **A. Attendre** : décaler la feature d'un trimestre ; prendre une feature secondaire à la
  place (en citer une du même backlog d'équipe si possible).
- **B. Réordonner** : garder le trimestre mais séquencer (l'équipe cible livre d'abord) ;
  préciser le sprint au plus tard et la marge.
- **C. Découpler** : contrat d'interface défini maintenant, mock côté équipe source,
  livraison derrière un feature flag activé quand l'équipe cible a livré.
Écarter un plan qui ne s'applique pas (par exemple B si la feature cible est prévue après
le trimestre) et dire pourquoi.

## Format de `decisions/propositions/<signal>.md`
1. Avertissement de simulacre.
2. Rappel du signal en 3 lignes.
3. Un tableau : plan, ce qui change, effet sur la charge (points, ratio), risque principal.
4. Pour chaque plan : conditions de réussite, et **où l'analyse doute**.
5. « Recommandation du point de vue des données » : un plan, une phrase, en rappelant que le
   choix revient au PM.
