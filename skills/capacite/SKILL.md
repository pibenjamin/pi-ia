---
name: capacite
description: Commenter le ratio capacité-charge par équipe calculé par scripts/capacite.py (disponibilités anonymisées, présents non disponibles, historique de livraison, anomalies par release). À utiliser pour écrire reports/capacite-<trimestre>-commentaire.md.
---

# Commentaire de capacité

Lire d'abord `skills/principes-communs.md`. Le calcul est fait par le script ; l'agent ne
recalcule pas, il explique.

## Rappel du calcul
capacité effective = (ETP disponibles x points par ETP et par sprint)
x taux de livraison historique x facteur qualité (anomalies pondérées par release,
rattachées à l'équipe qui a livré). Ratio = charge / capacité effective.

## Ce qu'il faut écrire
- Les équipes en `surcharge` et en `tension` : quelles épiques pèsent le plus, et ce qui
  change si l'on retire la plus grosse.
- Les équipes avec beaucoup de « présents mais pas disponibles sur le projet » : l'écart
  entre ETP nominal et ETP disponibles.
- L'effet des dépendances : une équipe en surcharge qui est aussi cible de signaux
  (voir `reports/signaux-*`) est un risque double.
- Où le calcul est fragile (historique court, anomalies d'une seule release, etc.).
Jamais de commentaire sur des personnes. Format : Markdown, 1 page maximum.
