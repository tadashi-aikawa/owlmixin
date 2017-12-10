MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Install dependencies and create envirionment
		@echo Start $@
		@pipenv install -d
		@echo End $@

_clean-docs: ## Clean documentation
		@cd sphinx-docs && pipenv run make clean

build-docs: _clean-docs ## Build documentation
		@echo Start $@
		@cd sphinx-docs && pipenv run make html linkcheck
		@echo End $@

_clean-package-docs: ## Clean package documentation
		@rm -rf docs/*

package-docs: build-docs _clean-package-docs ## Package documentation
		@echo Start $@
		@cp -r sphinx-docs/_build/html/* docs/
		@touch docs/.nojekyll
		@echo End $@

_clean-package: ## Clean package
		@echo Start $@
		@rm -rf build dist owlmixin.egg-info
		@echo End $@

package: _clean-package ## Package OwlMixin
		@echo Start $@
		@pipenv run python setup.py bdist_wheel
		@echo End $@

release: package ## Release OwlMixin (set RELEASE_VERSION, PYPI_PASSWORD)
		@echo Start $@
		@twine upload dist/owlmixin-$(RELEASE_VERSION)-py3-none-any.whl 
			--config-file ".pypirc"
			-u tadashi-aikawa \
			-p $(PYPI_PASSWORD)
		@echo End $@

test: ## Unit test
		@echo Start $@
		@pipenv run py.test -vv --cov-report=xml --cov=. tests/
		@echo End $@

doctest: ## Doc test
		@echo Start $@
		@pipenv run python -m doctest owlmixin/{__init__.py,transformers.py,owlcollections.py,owlenum.py,owloption.py} -v
		@echo End $@

