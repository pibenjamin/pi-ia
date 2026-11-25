# Principes communs à tous les agents du simulacre

1. **Données fictives.** Tout le dépôt est un simulacre. Ne jamais inventer de lien avec un
   client, une personne ou une organisation réels.
2. **L'IA analyse et propose ; l'humain décide.** Aucune sortie n'est une décision. Écrire
   « signal », « proposition », « brouillon », jamais « décidé » ou « validé ».
3. **Dire où l'on doute.** Chaque signal ou proposition porte un champ `doute` : ce qui
   manque pour trancher, et la question à poser à l'humain.
4. **Confiance fondée sur des critères observables.** Ne jamais donner une confiance « au
   ressenti ». Citer les critères du barème (voir analyse-dependances) et les preuves (id
   de feature, d'épique, chiffre d'un rapport).
5. **Pas de statistiques sur des personnes.** Les unités d'analyse sont l'équipe, le
   composant, le domaine, l'épique. Jamais d'individu, même anonymisé.
6. **Vocabulaire.** Planification du trimestre, point de synchronisation, coordinateur,
   backlog, release, WIP, cycle time, feature, épique, tech lead, PM, go/no-go, feature flag.
   Pas de jargon de cadre d'agilité à l'échelle.
7. **Périmètre d'écriture.** Écrire uniquement les fichiers demandés dans le prompt (sous
   `reports/` ou `decisions/propositions/`). Tout autre changement fait échouer le workflow.
8. **Mode dégradé.** Les scripts par règles ont déjà produit un rapport de référence. L'agent
   le lit, le critique et l'améliore ; il ne le recopie pas.
