MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "[REQUIRED ERROR] \`$*\` is required."; \
		exit 1; \
	fi

-include .env

#---- Basic

init-dev: ## Install dependencies and create envirionment
	@poetry install

test: ## Unit test
	@poetry run pytest -vv --doctest-modules --doctest-continue-on-failure --cov-report=xml --cov=.

#---- Docs

_clean-docs: ## Clean documentation
	@cd sphinx-docs && poetry run make clean

build-docs: _clean-docs ## Build documentation
	@cd sphinx-docs && poetry run make html linkcheck

serve-docs: build-docs ## Serve documentation
	@cd sphinx-docs/_build/html && poetry run python -m http.server

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

_package-docs: build-docs _clean-package-docs ## Package documentation
	@cp -r sphinx-docs/_build/html/* docs/
	@touch docs/.nojekyll

#---- Release

_package: ## Package OwlMixin
	@poetry build -f wheel

release: guard-version test _package-docs ## make release version=x.y.z
	@echo '0. Install packages from lockfile'
	@poetry install --no-root

	@echo '1. Version up'
	@poetry version $(version)

	@echo '2. Package documentation'
	@make _package-docs

	@echo '3. Staging and commit'
	git add pyproject.toml
	git add docs
	git commit -m ':package: Version $(version)'

	@echo '4. Tags'
	ghr v$(version)

	@echo '5. Package OwlMixin'
	@make _package

	@echo '6. Publish'
	@poetry publish

	@echo '7. Push'
	git push --tags
	git push

	@echo 'Success All!!'
