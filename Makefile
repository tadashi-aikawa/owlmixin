MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Install dependencies and create envirionment
		@echo Start install packages
		@pipenv install -d
		@echo End install packages

_clean-docs: ## Clean documentation
		@echo Start clean documentation
		@cd sphinx-docs && pipenv run make clean
		@echo End clean documentation

build-docs: _clean-docs ## Build documentation
		@echo Start build documentation
		@cd sphinx-docs && pipenv run make html linkcheck
		@echo End build documentation

_clean-package: ## Clean package documentation
		@echo Start clean documentation
		@rm -rf docs/*
		@echo End clean documentation

package-docs: build-docs _clean-package ## Package documentation
		@echo Start package documentation
		@cp -r sphinx-docs/_build/html/* docs/
		@touch docs/.nojekyll
		@echo End package documentation

