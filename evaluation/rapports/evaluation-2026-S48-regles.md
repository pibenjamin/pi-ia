# Évaluation contre la vérité terrain (source : regles, semaine 2026-S48)

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

- Dépendances injectées trouvées : **8 / 9**
- Faux positifs : **3 / 12** (25%)

## Signal par signal

| Signal | Confiance | Verdict | Dépendance | Piège |
|---|---|---|---|---|
| DEP-EP-201-EQ-C | haute | vrai | GT-02 | — |
| DEP-EP-303-EQ-D | haute | vrai | GT-05 | — |
| DEP-EP-601-EQ-C | haute | vrai | GT-07 | — |
| DEP-EP-102-EQ-F | haute | vrai | GT-01 | — |
| DEP-EP-301-EQ-D | haute | vrai | GT-04 | — |
| DEP-EP-203-EQ-D | moyenne | vrai | GT-03 | — |
| DEP-EP-104-EQ-E | basse | vrai | GT-09 | — |
| DEP-EP-401-EQ-F | basse | vrai | GT-06 | — |
| DEP-EP-501-EQ-A | basse | vrai | GT-09 | — |
| DEP-EP-301-EQ-E | basse | faux positif | — | PG-03 |
| DEP-EP-302-EQ-F | basse | faux positif | — | PG-04 |
| DEP-EP-502-EQ-C | basse | faux positif | — | PG-05 |

## Dépendances manquées

- GT-08 : EP-302 → EQ-F. Traçabilité réglementaire des mouvements : DOM-12 n'est pas coché. Attendu : manqué par les règles.

## Calibration de la confiance

La confiance n'est utile que si les signaux « haute » sont rarement faux.

| Confiance | Signaux | Faux positifs |
|---|---|---|
| haute | 5 | 0 |
| moyenne | 1 | 0 |
| basse | 6 | 3 |
