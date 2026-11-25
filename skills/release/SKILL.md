---
name: release
description: Rédiger le brouillon de dossier go/no-go d'une release à partir des preuves rassemblées par scripts/release.py (tests, non-régression, anomalies, plan de monitoring, retour arrière). La décision reste humaine.
---

# Dossier go/no-go

Lire d'abord `skills/principes-communs.md`.

## Entrées
`releases/<release>.yml`, `reports/release-<release>-preuves.json`, les épiques du
périmètre dans `backlog/epics/`.

## Format de `reports/release-<release>-dossier.md`
1. Avertissement : brouillon, la décision appartient au responsable release.
2. Proposition : go / go sous conditions / no-go, avec la confiance et les critères.
3. Preuves de non-régression : suite par suite ; pour un échec, l'épique et le risque.
4. Plan de monitoring : indicateurs et seuils de retour arrière par épique ; signaler toute
   épique sans plan et proposer des indicateurs.
5. Conditions proposées (par exemple : livrer avec le feature flag désactivé pour l'épique
   concernée).
6. Où l'analyse doute.
