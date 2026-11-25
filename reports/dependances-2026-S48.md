# Dépendances 2027-T1, semaine 2026-S48 (source : ia)

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

13 signaux à valider par les tech leads. Aucun n'est une décision : ce sont des propositions
fondées sur les critères observables du barème. Référence comparée : les signaux par règles
([dependances-2026-S48-regles.md](dependances-2026-S48-regles.md)). Détail complet dans
[signaux-2026-S48-ia.json](signaux-2026-S48-ia.json).

| Signal | Équipes | Domaines | Types | Confiance (score) | Doute |
|---|---|---|---|---|---|
| DEP-EP-201-EQ-C | EQ-B → EQ-C | DOM-06, DOM-05 | sequence-coordination, capacite-charge | haute (7) | FEAT-061 n'arrive qu'en 2027-T2 : décaler EP-201 ou livrer une version sans flux temps réel ? |
| DEP-EP-303-EQ-D | EQ-C → EQ-D | DOM-08 | connaissance, sequence-coordination, capacite-charge | haute (6) | FEAT-081 (EP-403) est en 2027-T2 : avancer EP-403 ou décaler EP-303 ? |
| DEP-EP-601-EQ-C | EQ-F → EQ-C | DOM-06, DOM-05 | sequence-coordination, capacite-charge | haute (5) | À quel sprint EP-302 expose-t-elle le modèle par site ? |
| DEP-EP-102-EQ-F | EQ-A → EQ-F | DOM-12, DOM-11 | connaissance, sequence-coordination | haute (5) | EP-602 (FEAT-121) peut-elle passer en début de trimestre ? |
| DEP-EP-301-EQ-D | EQ-C → EQ-D | DOM-07 | sequence-coordination, capacite-charge | haute (5) | À quel sprint EP-402 met-elle FEAT-071 à disposition ? |
| DEP-EP-203-EQ-D | EQ-B → EQ-D | DOM-08, DOM-07 | connaissance, capacite-charge | moyenne (4) | Le report en cas de remboursement passe-t-il par FEAT-081 (2027-T2) ? |
| DEP-EP-103-EQ-C | EQ-A → EQ-C | DOM-05 | connaissance, capacite-charge | moyenne (3) | CMP-05 distingue-t-il déjà l'auteur d'une réservation du titulaire du compte ? |
| DEP-EP-402-EQ-E | EQ-D → EQ-E | DOM-09 | connaissance, capacite-charge | moyenne (3) | Les modèles FEAT-092 (livrée) suffisent-ils pour les relances ? |
| DEP-EP-302-EQ-F | EQ-C → EQ-F | DOM-12 | connaissance | basse (2) | Quelles durées de conservation pour les mouvements de stock ? |
| DEP-EP-401-EQ-F | EQ-D → EQ-F | DOM-12 | connaissance | basse (2) | L'archivage actuel couvre-t-il les échéanciers ? |
| DEP-EP-104-EQ-E | EQ-A → EQ-E | DOM-09 | sequence-coordination, capacite-charge | basse (2) | Épique commune ou doublon avec EP-501 ? |
| DEP-EP-104-EQ-F | EQ-A → EQ-F | DOM-12 | connaissance | basse (2) | L'historique des consentements a-t-il une durée légale ? |
| DEP-EP-501-EQ-A | EQ-E → EQ-A | DOM-01 | sequence-coordination | basse (1) | Même question que DEP-EP-104-EQ-E. |

## Lecture

- **Deux blocages inter-trimestres.** EP-201 (FEAT-061) et EP-303 (FEAT-081) sont prévues en
  2027-T1 mais attendent des features prévues en 2027-T2. Sans arbitrage, elles ne peuvent pas
  être terminées dans le trimestre. Candidates pour `make plans`.
- **Trois séquences intra-trimestre.** EP-102 attend EP-602, EP-301 attend EP-402, EP-601 attend
  EP-302. Elles tiennent si les épiques fournisseuses sont placées en début de trimestre. Deux
  des trois fournisseurs sont dans des équipes à risque : EQ-C en surcharge (1.18) et EQ-D avec
  26 % de présents non disponibles.
- **EQ-D et EQ-C concentrent les dépendances entrantes** (3 signaux chacune avec EP-103), et
  EQ-E est l'équipe la plus chargée (1.27) tout en refaisant son moteur de notifications (EP-503).

## Écarts avec les règles

**Ajoutés (besoins décrits dans le texte, non vus par les règles)**
- **DEP-EP-103-EQ-C** : la délégation porte sur des droits de *réservation*, avec attribution de
  chaque action au compte délégué. DOM-05 n'est pas coché.
- **DEP-EP-402-EQ-E** : « relances au client » relève des notifications, DOM-09 non coché.
- **DEP-EP-104-EQ-F** : historique de consentements, une donnée personnelle conservée. C'est le
  lien appris DOM-01 → DOM-12 raté en 2026-T3. DOM-12 est coché à 30 %, sous le seuil.

**Requalifiés**
- **DEP-EP-302-EQ-F** : le signal des règles portait sur DOM-11 via FEAT-111, déjà livrée. Ce
  volet est écarté. Le signal est reporté sur DOM-12 : le texte exige une conservation
  réglementaire des mouvements de stock, et DOM-12 n'est pas coché. Score 1 → 2.
- **DEP-EP-201-EQ-C** et **DEP-EP-601-EQ-C** : type `connaissance` retiré, car l'équipe source a
  une expertise moyenne sur DOM-06, le domaine principal du lien. Scores 8 → 7 et 6 → 5,
  confiance haute inchangée.
- **DEP-EP-501-EQ-A** : le critère « lien déjà confirmé ou appris » est retiré. La règle l'a
  accordé à cause de la paire DOM-01 / DOM-12, présente dans l'épique mais sans rapport avec le
  lien DOM-09 → DOM-01. Score 2 → 1.
- **DEP-EP-104-EQ-E** : le score est conservé, mais la justification change. Le vrai sujet est
  l'épique commune avec EP-501, pas une livraison à attendre.

**Retirés**
- **DEP-EP-301-EQ-E** : FEAT-092 déjà livrée, simple utilisation.
- **DEP-EP-502-EQ-C** : lecture seule via FEAT-051, déjà livrée.

**Remarque sur le rapport backlog** : la paire EP-302 / EP-601, marquée « doublon potentiel »
par les règles, n'est pas un doublon. EP-601 consomme le modèle produit par EP-302, ce qui est
une dépendance de séquence (DEP-EP-601-EQ-C). La paire EP-104 / EP-501, en revanche, ressemble
bien à un même besoin porté par deux équipes.

**Sans signal** : EP-603 n'a pas d'équipe. Elle toucherait EQ-B (DOM-03) et EQ-E (DOM-09,
DOM-10, déjà en surcharge). L'ownership est à trancher avant toute analyse de dépendance.

## Questions pour les tech leads

1. **EQ-C** : FEAT-061 peut-elle être avancée en 2027-T1 malgré le ratio de 1.18 ? Sinon, EP-201
   passe-t-elle en 2027-T2 ? Et à quel sprint EP-302 expose-t-elle le modèle multi-sites
   attendu par EP-601 ?
2. **EQ-D** : EP-403 (avoirs partiels, 40 pts) peut-elle être avancée en 2027-T1 pour EP-303 ?
   À quel sprint EP-402 livre-t-elle FEAT-071 pour EP-301 ? Le report des remises au
   remboursement (EP-203) passe-t-il par FEAT-081 ?
3. **EQ-F** : EP-602 peut-elle être en début de trimestre pour EP-102 ? Les mouvements de stock
   (EP-302), les échéanciers (EP-401) et l'historique des consentements (EP-104) ont-ils des
   durées de conservation que l'archivage actuel ne couvre pas ?
4. **EQ-A et EQ-E** : EP-104 et EP-501 sont-elles une même épique ? Qui porte l'écran et le
   stockage des préférences ?
5. **EQ-E** : EP-503 refait le moteur utilisé par FEAT-091 (EP-101) et FEAT-092 (EP-301), et
   peut-être par les relances d'EP-402. Les consommateurs actuels sont-ils protégés pendant la
   refonte (compatibilité, feature flag) ?
6. **EQ-B et EQ-F** : la nouvelle structure des fiches (EP-202) garde-t-elle les identifiants
   utilisés par les statistiques de consultation ? Si non, il manque une dépendance vers EQ-F.
