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

lint: ## Lint
	@shopt -s globstar; uv run ruff check owlmixin/**/*.py

format: ## Format
	@shopt -s globstar; uv run ruff format owlmixin/**/*.py

test: ## Test
	@uv run pytest -vv --doctest-modules --doctest-continue-on-failure --cov-report=xml --cov=.

ci: ## lint & format & test & test-e2e
	@make lint format test

#---- Docs

_clean-docs: ## Clean documentation
	@cd sphinx-docs && uv run make clean

build-docs: _clean-docs ## Build documentation
	@cd sphinx-docs && uv run make html linkcheck

serve-docs: build-docs ## Serve documentation
	@cd sphinx-docs/_build/html && uv run python -m http.server

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

_package-docs: build-docs _clean-package-docs ## Package documentation
	@cp -r sphinx-docs/_build/html/* docs/
	@touch docs/.nojekyll

#---- Release

release: guard-version ## make release version=x.y.z
	@echo '0. Install packages from lockfile, then test and package documentation'
	@uv sync
	@make test _package-docs

	@echo '1. Version up'
	@sed -i 's/^version = ".*"/version = "$(version)"/' pyproject.toml

	@echo '2. Package documentation'
	@make _package-docs

	@echo '3. Staging and commit'
	git add pyproject.toml
	git add docs
	git commit -m ':package: Version $(version)'

	@echo '4. Tags'
	git tag v$(version) -m v$(version)

	@echo '5. Package OwlMixin'
	@uv build

	@echo '6. Publish'
	@uv publish

	@echo '7. Push'
	git push --tags
	git push

	@echo 'Success All!!'
