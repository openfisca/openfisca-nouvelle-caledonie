#!/bin/bash

# Script pour créer la Pull Request
# Assurez-vous d'être authentifié avec: gh auth login

TITLE="Renommage benefits en prestations_sociales et bump version 16.0.0"

BODY="## 16.0.0

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : \`parameters/benefits\`, \`variables/aide_logement.py\`, \`__init__.py\`.
* Détails :
  - Renommage du répertoire de paramètres \`benefits\` en \`prestations_sociales\` pour une meilleure cohérence terminologique.
  - Mise à jour de toutes les références dans le code (\`parameters(period).benefits\` → \`parameters(period).prestations_sociales\`).
  - **Breaking change** : Les chemins de paramètres ont changé (ex: \`benefits.aide_logement.*\` → \`prestations_sociales.aide_logement.*\`)."

gh pr create --title "$TITLE" --body "$BODY" --base main
