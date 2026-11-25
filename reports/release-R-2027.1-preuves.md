# Preuves de la release R-2027.1 (calcul par règles)

> Simulacre : données entièrement fictives. Ce rapport illustre une cible, pas un retour d'expérience.

Proposition des règles : **go sous conditions**. Brouillon : la décision reste humaine.

| Critère | Respecté | Détail |
|---|---|---|
| tests automatisés | oui | 1842 / 1842 réussis |
| couverture | oui | 78% (minimum 75%) |
| non-régression | **non** | archivage-legal : 2 cas sur 40 : purge d'un client avec litige en cours |
| anomalies bloquantes | oui | 0 bloquantes, 7 mineures ouvertes |
| plan de monitoring | **non** | sans plan : EP-602 |
| retour arrière | oui | Désactivation des feature flags ; EP-202 sans flag : redéploiement de la version précédente. (sans feature flag : EP-202) |

Périmètre : EP-103 (EQ-A), EP-202 (EQ-B), EP-402 (EQ-D), EP-602 (EQ-F)
