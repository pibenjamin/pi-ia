# Évaluation contre la vérité terrain (source : ia, semaine 2026-S48)

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

- Dépendances injectées trouvées : **9 / 9**
- Faux positifs : **3 / 13** (23%)

## Signal par signal

| Signal | Confiance | Verdict | Dépendance | Piège |
|---|---|---|---|---|
| DEP-EP-201-EQ-C | haute | vrai | GT-02 | — |
| DEP-EP-303-EQ-D | haute | vrai | GT-05 | — |
| DEP-EP-601-EQ-C | haute | vrai | GT-07 | — |
| DEP-EP-102-EQ-F | haute | vrai | GT-01 | — |
| DEP-EP-301-EQ-D | haute | vrai | GT-04 | — |
| DEP-EP-203-EQ-D | moyenne | vrai | GT-03 | — |
| DEP-EP-103-EQ-C | moyenne | faux positif | — | — |
| DEP-EP-402-EQ-E | moyenne | faux positif | — | — |
| DEP-EP-302-EQ-F | basse | vrai | GT-08 | PG-04 |
| DEP-EP-401-EQ-F | basse | vrai | GT-06 | — |
| DEP-EP-104-EQ-E | basse | vrai | GT-09 | — |
| DEP-EP-104-EQ-F | basse | faux positif | — | — |
| DEP-EP-501-EQ-A | basse | vrai | GT-09 | — |

## Dépendances manquées

Aucune.

## Calibration de la confiance

La confiance n'est utile que si les signaux « haute » sont rarement faux.

| Confiance | Signaux | Faux positifs |
|---|---|---|
| haute | 5 | 0 |
| moyenne | 3 | 2 |
| basse | 5 | 1 |
