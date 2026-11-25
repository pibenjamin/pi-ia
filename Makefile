# Mode dégradé et usage local : tout se fait sans IA et sans GitHub.
# Prérequis : Python 3.10+ et PyYAML (pip install -r requirements.txt).
PY ?= python3
SEMAINE ?= $(shell date +%G-S%V)
RELEASE ?= R-2027.1

.PHONY: aide tout verifier capacite dependances backlog evaluer flux release faux-positifs synthese plans test

aide:
	@echo "make tout            : toutes les analyses par règles + synthèse (SEMAINE=$(SEMAINE))"
	@echo "make dependances     : signaux de dépendance par règles"
	@echo "make evaluer         : comparaison à la vérité terrain du simulacre"
	@echo "make plans SIGNAL=DEP-EP-303-EQ-D : plans proposés au PM"
	@echo "make release RELEASE=R-2027.1     : preuves go/no-go"
	@echo "make verifier        : contrôle d'anonymisation (avant chaque commit)"
	@echo "make test            : tests"

tout: verifier capacite dependances backlog evaluer flux release faux-positifs synthese

verifier:
	$(PY) scripts/anonymiser.py verifier
capacite:
	$(PY) scripts/capacite.py
dependances:
	$(PY) scripts/dependances.py --semaine $(SEMAINE)
backlog:
	$(PY) scripts/backlog.py --semaine $(SEMAINE)
evaluer:
	$(PY) scripts/evaluer.py reports/signaux-$(SEMAINE)-regles.json
flux:
	$(PY) scripts/flux.py
release:
	$(PY) scripts/release.py $(RELEASE)
faux-positifs:
	$(PY) scripts/faux_positifs.py
synthese:
	$(PY) scripts/synthese.py
plans:
	$(PY) scripts/plans.py $(SIGNAL)
test:
	$(PY) -m unittest discover -s tests -v
