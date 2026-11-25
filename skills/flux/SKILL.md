---
name: flux
description: Expliquer une dérive de flux (WIP au-dessus de la limite, cycle time qui s'allonge, tickets qui stagnent) à partir de reports/flux-<semaine>.json, et proposer des actions. Déclenché par événement, pas en continu.
---

# Analyse de flux

Lire d'abord `skills/principes-communs.md`.

## Entrées
`reports/flux-<semaine>.json` (WIP, cycle time médian et p85, tickets qui stagnent par
équipe), `reports/capacite-<trimestre>.json`, les signaux de dépendance récents.

## Ce qu'il faut écrire dans `reports/flux-<semaine>-commentaire.md`
- Pour chaque alerte : hypothèse d'explication **reliée à une donnée** (une dépendance
  signalée vers l'équipe, une surcharge, un ticket bloqué), et le niveau de confiance.
- 2 ou 3 actions possibles par équipe concernée (arrêter de démarrer, finir les tickets
  bloqués, point de synchronisation avec l'équipe dont on attend une livraison).
- Ce que les données ne permettent pas de dire.
Unité d'analyse : l'équipe et le ticket. Jamais de personne.
