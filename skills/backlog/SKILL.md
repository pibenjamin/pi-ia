---
name: backlog
description: Repérer les faiblesses du backlog (doublons, épiques communes, dépendances potentielles, ownership flou, feature trop grosse, manque d'informations) à partir des épiques et du rapport par règles.
---

# Analyse des backlogs

Lire d'abord `skills/principes-communs.md`.

Partir de `reports/backlog-<semaine>-regles.json`. Pour chaque faiblesse, dire si elle est
confirmée par le texte des épiques, et formuler **une question** à poser à l'équipe (pas un
jugement). Ajouter ce que les règles ne voient pas (par exemple deux épiques dont les
textes décrivent le même besoin avec des domaines cochés différents).
Sortie : section « Faiblesses du backlog » à la fin de `reports/dependances-<semaine>.md`.
