# Choix, limites et questions ouvertes

## Questions ouvertes du brief : choix faits

| Question | Choix pour le simulacre | Pourquoi | Réversible ? |
|---|---|---|---|
| Format du tableau de synthèse | `reports/SYNTHESE.md`, recopié dans le résumé du run d'orchestration | Aucun outil en plus, lisible sur GitHub, fonctionne en mode dégradé, versionné | Oui : un site (GitHub Pages) pourrait lire les mêmes JSON |
| Épiques en fichiers ou en issues | Fichiers `backlog/epics/*.md` ; les **signaux** sont des issues | Les épiques sont des données d'entrée versionnées (diff, historique, mode hors ligne) ; les signaux appellent une action humaine, d'où les issues et les étiquettes | Oui : un formulaire d'issue pourrait produire les mêmes fichiers |
| Dépôt public ou privé | À décider par l'utilisateur | Public : cron désactivé après 60 jours sans activité, minutes gratuites. Privé : minutes décomptées, relecteurs obligatoires des environnements selon l'offre | — |

Restent ouvertes (hors dépôt) : quels agents ont réellement tourné chez l'assureur et
comment (pour ne pas surdéclarer) ; l'ordre de grandeur chiffré du stock de features non
terminées.

## Comment l'IA est encadrée

- Outils minimaux : lecture et écriture de fichiers, pas de shell, pas d'API GitHub
  (`--allowedTools Read,Glob,Grep,Write,Edit`, `--permission-mode default`).
- Périmètre d'écriture vérifié après chaque appel (`scripts/verifier_perimetre.sh`).
- La vérité terrain (`evaluation/`) est supprimée de l'espace de travail avant l'appel.
- Les tickets, commits et journaux sont produits par des scripts déterministes, pas par
  l'agent.
- Sortie contrôlée par un format JSON ; si elle est invalide, retour aux règles.
- Coût borné : `--max-turns`, `timeout-minutes`, appel seulement sur événement pour le flux
  et la capacité (seulement s'il y a un écart).

## Confiance : critères observables

Le score n'est pas demandé au modèle « au ressenti ». Il additionne des critères vérifiables
(certitude du cochage, feature citée non livrée, lien déjà confirmé, absence d'expertise,
surcharge de l'équipe cible, etc.). Sur les données fournies, les règles donnent 0 faux
positif en confiance haute et 3 sur 6 en confiance basse. Ce calibrage est à revérifier
chaque trimestre avec les validations des tech leads (`reports/faux-positifs-*.md`).

## Limites connues

- Les données sont petites et construites pour la démonstration : les chiffres obtenus ne
  disent rien des performances sur un vrai backlog.
- Le facteur qualité de la capacité (anomalies par release) et le coût forfaitaire du mock
  (plan C) sont des conventions, pas des mesures.
- La correspondance compte GitHub → rôle repose sur un fichier déclaratif ; avec
  `EXIGER_ROLES=true`, une validation d'un compte sans rôle est refusée.
- Les workflows n'ont pas encore tourné sur GitHub (voir [mise-en-place.md](mise-en-place.md)).

## Vigilances

- Ne pas confondre simulacre et retour d'expérience : avertissement en tête du dépôt et de
  chaque rapport.
- Données réelles qui s'y glissent : `make verifier` avant chaque commit (adresses
  électroniques, colonnes nominatives, liste noire locale `entrees/liste-noire.txt` non
  versionnée), et le même contrôle tourne dans `controles.yml`.
- Pas de performance individuelle : toutes les mesures sont par équipe, composant, domaine
  ou épique. En contexte réel, consultation possible du CSE et analyse au regard de
  l'AI Act (à vérifier).
- Si l'on branche un jour les outils d'un client : réseau interne, accord sur le passage des
  données par GitHub et Anthropic.
