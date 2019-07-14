MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

-include .env

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

version := $(shell git rev-parse --abbrev-ref HEAD)

#------

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

serve-docs: build-docs ## Serve documentation
	@echo Start $@
	@cd sphinx-docs/_build/html && pipenv run python -m http.server
	@echo End $@

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

_package-docs: build-docs _clean-package-docs ## Package documentation
	@echo Start $@
	@cp -r sphinx-docs/_build/html/* docs/
	@touch docs/.nojekyll
	@echo End $@

test: ## Unit test
	@echo Start $@
	@pipenv run python -m pytest -vv --cov-report=xml --cov=. tests/
	@echo End $@

doctest: ## Doc test
	@echo Start $@
	@pipenv run python -m doctest owlmixin/{__init__.py,transformers.py,owlcollections.py,owlenum.py,owloption.py,util.py} -v
	@echo End $@

_clean-package: ## Clean package
	@echo Start $@
	@rm -rf build dist owlmixin.egg-info
	@echo End $@

_package: _clean-package ## Package OwlMixin
	@echo Start $@
	@pipenv run python setup.py bdist_wheel
	@echo End $@

release: _package-docs ## Release (set TWINE_USERNAME and TWINE_PASSWORD to enviroment varialbles)

	@echo '0. Install packages from lockfile and test'
	@pipenv install --deploy
	@make test
	@make doctest

	@echo '1. Recreate `owlmixin/version.py`'
	@echo "__version__ = '$(version)'" > owlmixin/version.py

	@echo '2. Package documentation'
	@make _package-docs

	@echo '3. Staging and commit'
	git add owlmixin/version.py
	git add docs
	git commit -m ':package: Version $(version)'

	@echo '4. Tags'
	git tag v$(version) -m v$(version)

	@echo '5. Deploy'
	@echo 'Packageing...'
	@pipenv run python setup.py bdist_wheel
	@echo 'Deploying...'
	@pipenv run twine upload dist/owlmixin-$(version)-py3-none-any.whl

	@echo '6. Push'
	git push --tags
	git push

	@echo 'Success All!!'
	@echo 'Create a pull request and merge to master!!'
	@echo 'https://github.com/tadashi-aikawa/owlmixin/compare/$(version)?expand=1'

