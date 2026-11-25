# Déroulé de la démonstration (environ 15 minutes)

Rappeler d'abord, en une phrase : **simulacre, données fictives ; le cas réel reposait sur
des exports manuels et du copier-coller.**

## 1. Les données (2 min)

- `domains/domains.yml` : 12 domaines issus d'un atelier Event Storming (simulé).
- Une épique, par exemple `backlog/epics/EP-201.md` : l'équipe a coché les domaines touchés
  avec un degré de certitude (DOM-04 100 %, DOM-06 100 %, DOM-05 50 %).
- `history/features.yml` : la question clé de la dépendance de séquence, « la feature dont
  on dépend est-elle déjà implémentée ? ».

## 2. L'analyse des dépendances (4 min)

Lancer *Actions → 1. Dépendances* (ou montrer un run déjà fait).

- Les règles produisent `reports/dependances-AAAA-SS-regles.md` : chaque signal a un type
  (connaissance, capacité-charge, séquence et coordination) et un score de confiance avec
  ses critères observables.
- Claude relit, écarte, requalifie, ajoute : `reports/dependances-AAAA-SS.md`, avec une
  section « où l'analyse doute ».
- Un ticket par signal, étiqueté par type et par confiance.

Point fort à montrer : l'**évaluation contre la vérité terrain** (résumé du run, ou
`evaluation/rapports/*.md`) : chaque dépendance injectée est trouvée ou manquée de façon
traçable, et la confiance est comparée aux faux positifs.

## 3. La validation et la décision (4 min)

- Sur un ticket, poser `validation:ecartee` (par exemple `DEP-EP-502-EQ-C` : la feature
  existe déjà). Le ticket se ferme, le journal `validation/journal.csv` reçoit une ligne,
  le commit nomme le rôle.
- Sur `DEP-EP-303-EQ-D`, poser `validation:confirmee`. Les plans arrivent dans
  `decisions/propositions/DEP-EP-303-EQ-D.md` : ici le plan B (réordonner) est écarté parce
  que la feature attendue est prévue au trimestre suivant.
- Lancer *3b. Décision du PM* avec le plan conseillé ; le PM approuve dans l'environnement
  `decision-pm`. Montrer l'historique Git : qui a conseillé, qui a décidé.

## 4. Capacité, flux, release (3 min)

- `reports/capacite-2027-T1.md` : EQ-C en surcharge (taux de livraison et anomalies pris en
  compte), EQ-D avec 26 % de « présents mais pas disponibles sur le projet ».
- `reports/flux-AAAA-SS.md` : WIP de EQ-C au-dessus de la limite, tickets qui stagnent ;
  Claude n'est appelé que parce qu'il y a une dérive.
- `reports/release-R-2027.1-preuves.md` : « go sous conditions » (une suite de
  non-régression en échec, une épique sans plan de monitoring).

## 5. Le mode dégradé (2 min)

Relancer *0. Orchestration* en décochant « Utiliser les agents IA » : tout tourne, la
synthèse indique « règles (mode dégradé) ». En local : `make tout`. Voir
[mode-degrade.md](mode-degrade.md).

## Phrases à garder en tête

- « L'IA analyse et propose, l'humain décide ; chaque décision a un responsable par rôle. »
- « La confiance n'est pas auto-déclarée : elle repose sur des critères observables et on
  la vérifie chaque trimestre avec les faux positifs. »
- « Une dépendance ratée enrichit la carte. »
- Ne pas présenter de chiffre du simulacre comme un résultat du cas réel.
