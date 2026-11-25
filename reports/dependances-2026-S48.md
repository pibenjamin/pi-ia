# Dépendances 2027-T1, semaine 2026-S48 (source : regles)

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

12 signaux à valider par les tech leads. Aucun n'est une décision.

| Signal | Équipes | Domaines | Types | Confiance (score) | Doute |
|---|---|---|---|---|---|
| DEP-EP-201-EQ-C | EQ-B → EQ-C | DOM-06, DOM-05 | connaissance, sequence-coordination, capacite-charge | haute (8) | — |
| DEP-EP-303-EQ-D | EQ-C → EQ-D | DOM-08 | connaissance, sequence-coordination, capacite-charge | haute (6) | — |
| DEP-EP-601-EQ-C | EQ-F → EQ-C | DOM-05, DOM-06 | connaissance, sequence-coordination, capacite-charge | haute (6) | — |
| DEP-EP-102-EQ-F | EQ-A → EQ-F | DOM-12, DOM-11 | connaissance, sequence-coordination | haute (5) | — |
| DEP-EP-301-EQ-D | EQ-C → EQ-D | DOM-07 | sequence-coordination, capacite-charge | haute (5) | — |
| DEP-EP-203-EQ-D | EQ-B → EQ-D | DOM-07, DOM-08 | connaissance, capacite-charge | moyenne (4) | — |
| DEP-EP-104-EQ-E | EQ-A → EQ-E | DOM-09 | sequence-coordination, capacite-charge | basse (2) | Aucune preuve dans le texte : signal fondé sur le seul cochage. |
| DEP-EP-401-EQ-F | EQ-D → EQ-F | DOM-12 | connaissance | basse (2) | — |
| DEP-EP-501-EQ-A | EQ-E → EQ-A | DOM-01 | sequence-coordination | basse (2) | Aucune preuve dans le texte : signal fondé sur le seul cochage. |
| DEP-EP-301-EQ-E | EQ-C → EQ-E | DOM-09 | connaissance, capacite-charge | basse (1) | Les features citées existent déjà : le besoin restant est peut-être nul. |
| DEP-EP-302-EQ-F | EQ-C → EQ-F | DOM-11 | connaissance | basse (1) | Les features citées existent déjà : le besoin restant est peut-être nul. |
| DEP-EP-502-EQ-C | EQ-E → EQ-C | DOM-05 | connaissance, capacite-charge | basse (1) | Les features citées existent déjà : le besoin restant est peut-être nul. |

## Détail des critères

- **DEP-EP-201-EQ-C** (Tarification dynamique selon la disponibilité) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché à 100 % ; cite une feature de l'équipe cible non livrée ; la feature citée est prévue après le trimestre de l'épique, ou non planifiée ; lien entre ces domaines déjà confirmé ou appris. Preuves : FEAT-061 (Flux de disponibilité temps réel, planifiee 2027-T2)
- **DEP-EP-303-EQ-D** (Gestion des retours anticipés) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; cite une feature de l'équipe cible non livrée ; la feature citée est prévue après le trimestre de l'épique, ou non planifiée. Preuves : FEAT-081 (Avoirs partiels, planifiee 2027-T2)
- **DEP-EP-601-EQ-C** (Tableau de bord de pilotage des locations) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; cite une épique de l'équipe cible ; lien entre ces domaines déjà confirmé ou appris. Preuves : EP-302 (Inventaire multi-sites, 2027-T1)
- **DEP-EP-102-EQ-F** (Suppression de compte à la demande du client) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; domaine coché entre le seuil et 99 % ; cite une feature de l'équipe cible non livrée ; lien entre ces domaines déjà confirmé ou appris. Preuves : FEAT-121 (Purge sélective des archives, planifiee 2027-T1)
- **DEP-EP-301-EQ-D** (Réservation récurrente) : équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; cite une feature de l'équipe cible non livrée ; lien entre ces domaines déjà confirmé ou appris. Preuves : FEAT-071 (Prélèvement récurrent, planifiee 2027-T1)
- **DEP-EP-203-EQ-D** (Codes promotionnels) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; lien entre ces domaines déjà confirmé ou appris
- **DEP-EP-104-EQ-E** (Gestion des consentements de communication) : équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 %
- **DEP-EP-401-EQ-F** (Paiement en plusieurs fois) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; domaine coché entre le seuil et 99 %
- **DEP-EP-501-EQ-A** (Centre de préférences de contact) : domaine coché entre le seuil et 99 % ; lien entre ces domaines déjà confirmé ou appris
- **DEP-EP-301-EQ-E** (Réservation récurrente) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; ne cite que des features déjà livrées. Preuves : FEAT-092 (Modèles de notification paramétrables, livree 2026-T3)
- **DEP-EP-302-EQ-F** (Inventaire multi-sites) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; domaine coché entre le seuil et 99 % ; ne cite que des features déjà livrées ; lien entre ces domaines déjà confirmé ou appris. Preuves : FEAT-111 (Export libre-service des données de stock, livree 2026-T4)
- **DEP-EP-502-EQ-C** (Assistant de support en libre-service) : l'équipe de l'épique n'a pas d'expertise sur le domaine ; équipe cible en surcharge ou trop de présents non disponibles ; domaine coché entre le seuil et 99 % ; ne cite que des features déjà livrées. Preuves : FEAT-051 (API de lecture des réservations, livree 2026-T2)

## Candidats écartés

- EP-502 → EQ-A (DOM-01) : expertise présente et features citées déjà livrées : FEAT-011

Barème de confiance : domaine coché à 100 % (+2) ; domaine coché entre le seuil et 99 % (+1) ; cite une feature de l'équipe cible non livrée (+2) ; la feature citée est prévue après le trimestre de l'épique, ou non planifiée (+1) ; cite une épique de l'équipe cible (+2) ; ne cite que des features déjà livrées (-2) ; lien entre ces domaines déjà confirmé ou appris (+1) ; l'équipe de l'épique n'a pas d'expertise sur le domaine (+1) ; équipe cible en surcharge ou trop de présents non disponibles (+1).
