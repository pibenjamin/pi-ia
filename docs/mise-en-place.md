# Mise en place sur GitHub

Rien de ceci n'a encore été exécuté : c'est la liste des réglages nécessaires, à vérifier
au premier lancement.

## 1. Branche par défaut

Les workflows planifiés (`schedule`) ne tournent que depuis la branche par défaut, et les
déclencheurs `push` de `capacite.yml`, `flux.yml` et `release.yml` sont limités à `main`.
Fusionner ce travail dans `main` et en faire la branche par défaut.

Dépôt public : le cron est désactivé après 60 jours sans activité. Dépôt privé : les minutes
Actions sont décomptées. Voir [choix-et-limites.md](choix-et-limites.md).

## 2. Secret d'authentification de Claude

Dans *Settings → Secrets and variables → Actions → Secrets*, créer **un** des deux :

- `ANTHROPIC_API_KEY` (clé d'API Anthropic), ou
- `CLAUDE_CODE_OAUTH_TOKEN`.

Jamais de secret dans le dépôt. Sans secret, les workflows tournent quand même, en mode
dégradé (règles seules), et l'écrivent dans le résumé du run.

## 3. Variables (facultatives)

*Settings → Secrets and variables → Actions → Variables* :

| Variable | Effet | Défaut |
|---|---|---|
| `AGENTS_IA_ACTIFS` | `false` coupe l'IA dans tous les workflows (mode dégradé) | actif si un secret existe |
| `CLAUDE_MODELE` | modèle utilisé par les agents | `claude-sonnet-5-5` |
| `EXIGER_ROLES` | `true` refuse une validation ou une décision d'un compte sans le bon rôle | non exigé |

## 4. Rôles

Renseigner `gouvernance/roles.yml` : le compte GitHub qui joue chaque rôle (PM,
coordinateur, tech leads, responsable release). Pour une démonstration en solo, un même
compte peut tenir tous les rôles ; le journal affiche alors `PM+COORDINATEUR+TL-EQ-A+...`.

## 5. Environnements d'approbation

*Settings → Environments* :

- `decision-pm` : *Required reviewers* = le compte du PM. Utilisé par `decision-pm.yml`.
- `go-no-go` : *Required reviewers* = le responsable release. Utilisé par `release-decision.yml`.

Selon l'offre GitHub, les relecteurs obligatoires ne sont pas disponibles pour tous les
types de dépôts privés : à vérifier pour le compte utilisé.

## 6. Permissions des workflows

*Settings → Actions → General → Workflow permissions* : autoriser l'écriture
(« Read and write permissions ») pour que les workflows puissent commiter les rapports et
ouvrir des tickets. Chaque workflow déclare de toute façon ses permissions minimales.

## 7. Points à vérifier au premier lancement

- `anthropics/claude-code-action@v1` reçoit `github_token: ${{ github.token }}` pour ne pas
  dépendre de l'application GitHub Claude. La documentation de l'action réserve ce champ à
  une application GitHub personnalisée : si l'action refuse ce jeton, installer
  l'application Claude sur le dépôt et retirer la ligne (`.github/actions/agent-claude/action.yml`).
- L'agent tourne en `--permission-mode default` avec `--allowedTools Read,Glob,Grep,Write,Edit` :
  pas de shell, pas d'API GitHub. Le périmètre d'écriture est contrôlé après coup par
  `scripts/verifier_perimetre.sh` (le workflow échoue si l'agent écrit ailleurs).
- `--max-turns` (15 par défaut, 8 à 10 selon l'agent) et `timeout-minutes` bornent le coût.
- Les commits faits avec le `GITHUB_TOKEN` ne déclenchent pas d'autres workflows : c'est
  voulu (pas de boucle), et c'est pourquoi l'orchestration enchaîne les étapes par
  `workflow_call` plutôt que par des commits.

## 8. Brancher un outil de suivi (cas réel futur, hors simulacre)

Une règle d'automatisation de l'outil de suivi envoie une requête web vers l'API
« repository dispatch » de GitHub (`POST /repos/{owner}/{repo}/dispatches`,
`event_type: export-flux`), avec un jeton qui a le droit d'écriture sur le dépôt.
`flux.yml` écoute déjà cet événement. Le simulacre s'en passe : il lit des fichiers.
Avant tout branchement réel : réseau interne, accord sur le passage des données par
GitHub et Anthropic, anonymisation en amont (`scripts/anonymiser.py transformer`).
