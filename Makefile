# Regenerate and verify the README artwork. Needs only Python 3.10+.
PY ?= python3

.PHONY: build check test preview

build:   ## regenerate every SVG in assets/
	$(PY) scripts/build.py

check:   ## fail if assets/ is out of date
	$(PY) scripts/build.py --check

test:    ## run the asset and README checks
	$(PY) -m unittest discover -s tests

preview: ## serve the repo at http://localhost:8000 to eyeball the SVGs
	$(PY) -m http.server 8000
