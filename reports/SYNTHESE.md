# Tableau de synthèse, planification 2027-T1

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

Chaque ligne renvoie au rapport détaillé. Les décisions sont dans les journaux versionnés.

## 1. Dépendances

Source : **règles (mode dégradé)**, semaine 2026-S48 ([JSON](signaux-2026-S48-regles.json)).

| Signal | Types | Confiance | Validation tech lead |
|---|---|---|---|
| DEP-EP-201-EQ-C | connaissance, sequence-coordination, capacite-charge | haute | à valider |
| DEP-EP-303-EQ-D | connaissance, sequence-coordination, capacite-charge | haute | à valider |
| DEP-EP-601-EQ-C | connaissance, sequence-coordination, capacite-charge | haute | à valider |
| DEP-EP-102-EQ-F | connaissance, sequence-coordination | haute | à valider |
| DEP-EP-301-EQ-D | sequence-coordination, capacite-charge | haute | à valider |
| DEP-EP-203-EQ-D | connaissance, capacite-charge | moyenne | à valider |
| DEP-EP-104-EQ-E | sequence-coordination, capacite-charge | basse | à valider |
| DEP-EP-401-EQ-F | connaissance | basse | à valider |
| DEP-EP-501-EQ-A | sequence-coordination | basse | à valider |
| DEP-EP-301-EQ-E | connaissance, capacite-charge | basse | à valider |
| DEP-EP-302-EQ-F | connaissance | basse | à valider |
| DEP-EP-502-EQ-C | connaissance, capacite-charge | basse | à valider |

_Simulacre uniquement_ : contre la vérité terrain, 8 / 9 dépendances injectées trouvées, 3 faux positifs sur 12 signaux ([évaluation](../evaluation/rapports/evaluation-2026-S48-regles.md)).

Faux positifs du trimestre : **—** (0 écartés sur 0 validés) ; dépendances ratées : **0** ([détail](faux-positifs-2027-T1.md)).

## 2. Décisions du PM

Aucune décision enregistrée.

## 3. Capacité-charge

| Équipe | Ratio charge / capacité | État | Présents non dispo |
|---|---|---|---|
| EQ-A | 0.88 | tension | 0% |
| EQ-B | 0.79 | ok | 2% |
| EQ-C | 1.18 | surcharge | 0% |
| EQ-D | 0.88 | tension | 26% |
| EQ-E | 1.27 | surcharge | 0% |
| EQ-F | 0.61 | ok | 10% |

[Détail](capacite-2027-T1.md)

## 4. Flux

Semaine 2026-S48 : 4 alerte(s). [Détail](flux-2026-S48.md)

- EQ-C : WIP 11 au-dessus de la limite 6
- EQ-C : TK-106 (en-cours) sans mouvement depuis 16 j
- EQ-C : TK-107 (bloque) sans mouvement depuis 12 j
- EQ-E : TK-108 (bloque) sans mouvement depuis 14 j

## 5. Backlog

- EP-503 : trop-grosse
- EP-603 : ownership-flou
- EP-503 : manque-informations
- EP-104, EP-501 : doublon-potentiel
- EP-302, EP-601 : doublon-potentiel

## 6. Release

R-2027.1 : proposition des règles **go sous conditions** (critères non respectés : non-régression, plan de monitoring). [Preuves](release-R-2027.1-preuves.md)
Décision humaine : en attente.
