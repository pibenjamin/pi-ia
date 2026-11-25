#!/usr/bin/env bash
# Échoue si des fichiers ont été modifiés hors des chemins autorisés.
# Usage : scripts/verifier_perimetre.sh reports/ decisions/propositions/
# Sert après chaque appel à Claude : l'agent ne doit écrire que ses rapports.
set -euo pipefail
autorises=("$@")
hors=()
while IFS= read -r f; do
  [ -z "$f" ] && continue
  ok=false
  for a in "${autorises[@]}"; do
    [[ "$f" == "$a"* ]] && ok=true
  done
  $ok || hors+=("$f")
done < <(git status --porcelain --untracked-files=all | sed -E 's/^.. //; s/.* -> //')
if [ ${#hors[@]} -gt 0 ]; then
  echo "Modifications hors périmètre (${autorises[*]}) :" >&2
  printf ' - %s\n' "${hors[@]}" >&2
  exit 1
fi
echo "Périmètre respecté (${autorises[*]})."
