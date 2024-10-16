.PHONY: all clean clean-test clean-pyc clean-build docs help test
.DEFAULT: help

SHELL := /bin/bash

# These variables can be passed from the command line when invoking make.
PREFIX		= /usr/local

GITHUB_USER = ReliaQualAssociates
TOKEN		= $(shell echo $(GITHUB_TOKEN))
REPO		= ramstk

SRCFILE		= src/ramstk/
VIRTBASE	= $(shell echo $(HOME))/.venvs
ROOT 		= $(shell git rev-parse --show-toplevel)
WORKBRANCH  = $(shell git rev-parse --abbrev-ref HEAD)

# Shell commands:
PYTHON		= $(shell which python)
PY			= $(shell which python -V | cut -d ' ' -f2)
COPY 		= cp -v
MKDIR 		= mkdir -pv
MV			= mv -v
RM			= rm -fv
RMDIR		= rm -fvr
SED			= sed
GIT			= $(shell which git)

BLACK		= $(shell which black)
CHKMANI		= $(shell which check-manifest)
DOCFORMATTER	= $(shell which docformatter)
ISORT       = $(shell which isort)
MYPY		= $(shell which mypy)
POETRY		= $(shell which poetry)
PYCODESTYLE	= $(shell which pycodestyle)
PYDOCSTYLE	= $(shell which pydocstyle)
PYLINT		= $(shell which pylint)
PYROMA		= $(shell which pyroma)
RADON		= $(shell which radon)
RSTCHECK	= $(shell which rstcheck)
RUFF		= $(shell which ruff)
TWINE		= $(shell which twine)

# Data files.
LAYOUTS		= $(shell ls ./data/layouts)
ICONS16		= $(shell ls ./data/icons/16x16)
ICONS32		= $(shell ls ./data/icons/32x32)

# Argument lists for tools.
DOCFORMATTER_ARGS	= --in-place --config ./pyproject.toml
ISORT_ARGS	= --settings-file ./pyproject.toml --atomic
MYPY_ARGS	= --config-file ./pyproject.toml
PYCODESTYLE_ARGS	= --count --config=./setup.cfg
PYDOCSTYLE_ARGS	= --count --config=./pyproject.toml
PYLINT_ARGS	= -j0 --rcfile=./pyproject.toml
RUFF_ARGS =

PYVERS		= 3.10 3.11 3.12

help:
	@echo "You can use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "Targets related to static code checking tools (good for IDE integration):"
	@echo "	format SRCFILE=<file>			format using black, isort, and docformatter.  Helpful to keymap in IDE or editor."
	@echo "	stylecheck SRCFILE=<file>		check using pycodestyle and pydocstyle.  Helpful to keymap in IDE or editor."
	@echo "	typecheck SRCFILE=<file>		check using mypy.  Helpful to keymap in IDE or editor."
	@echo "	typecheck.report			create an html report of source file typing coverage."
	@echo "	lint SRCFILE=<file>			lint using pylint.  Helpful to keymap in IDE or editor."
	@echo "						If passing a directory, all files will be recusively checked."
	@echo "	maintain SRCFILE=<file>			check maintainability using mccabe and radon.  Helpful to keymap in IDE or editor."
	@echo "						Pass wildcard (*) at end of FILE=<file> path to analyze all files in directory."
	@echo ""
	@echo "Targets related to documentation:"
	@echo "	docs					build API and user documentation."
	@echo ""
	@echo "Other targets:"
	@echo "	clean					removes all build, test, coverage, and Python artifacts."
	@echo "	install 				install RAMSTK and all data files in the current (virtualenv) environment."
	@echo "	install.dev				install only the RAMSTK code in the current (virtualenv) environment."
	@echo "	uninstall 				remove RAMSTK from the current (virtualenv) environment."
	@echo "	build					build source and wheel packages."
	@echo "	release					package and upload a release to PyPi."
	@echo ""
	@echo "The following variables are recognized by this Makefile.  They can be changed in this file or passed on the command line."
	@echo ""
	@echo "	GITHUB_USER				set the name of the Github user.  Defaults to $(GITHUB_USER)"
	@echo "	PYVERS					set the list of Python versions to test with in test.all.  Defaults to $(PYVERS)"
	@echo "	REPO					set the name of the GitHub repository to generate the change log from.  Defaults to $(REPO)"
	@echo "	SRCFILE					set the file or directory to static code check.  Defaults to $(SRCFILE)"
	@echo "	TOKEN					set the Github API token to use.  Defaults to environment variable GITHUB_TOKEN"
	@echo "	VIRTBASE				set the name of the base directory for virtual environments.  Defaults to $(VIRTBASE)."

# Targets for cleaning up after yourself.
clean: clean-build clean-docs clean-pyc clean-test		## removes all build, test, coverage, and Python artifacts

clean-build:	## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(shell find . -name '*.egg-info' -exec rm -fr '{}' +)
	$(shell find . -name '*.egg' -exec rm -fr '{}' +)

clean-docs:
	cd docs; rm -fr _build/html/*

clean-pyc:		## remove Python file artifacts
	$(shell find . -name '*.pyc' -exec rm -f {} +)
	$(shell find . -name '*.pyo' -exec rm -f {} +)
	$(shell find . -name '*~' -exec rm -f {} +)
	$(shell find . -name '__pycache__' -exec rm -fr {} +)

clean-test:	clean-pyc	## remove test and coverage artifacts
	@echo -e "\n\t\033[1;36mCleaning up old test run artifacts ...\033[0m\n"
	rm -fr .tox/
	rm -f .coverage
	rm -fr .reports/coverage
	rm -fr .pytest_cache

# Targets to install and uninstall RAMSTK.
install: clean-build clean-pyc
	@echo -e "\n\t\033[1;32mInstalling RAMSTK and all data files to $(PREFIX) ...\033[0m\n"
	pip install . --prefix=$(PREFIX)
	${MKDIR} "$(PREFIX)/share/RAMSTK"
	${MKDIR} "$(PREFIX)/share/RAMSTK/layouts"
	${MKDIR} "$(PREFIX)/share/RAMSTK/icons/16x16"
	${MKDIR} "$(PREFIX)/share/RAMSTK/icons/32x32"
	${MKDIR} "$(PREFIX)/share/RAMSTK/logs"
	${MKDIR} "$(PREFIX)/share/doc/ramstk"
	${MKDIR} "$(PREFIX)/share/applications"
	${MKDIR} "$(PREFIX)/share/pixmaps"
	${COPY} "./data/RAMSTK.desktop" "$(PREFIX)/share/applications"
	${COPY} "./data/icons/RAMSTK.png" "$(PREFIX)/share/pixmaps"
	${COPY} "./README.md" "$(PREFIX)/share/doc/ramstk"
	for file in ${LAYOUTS} ; do \
		${COPY} "./data/layouts/$$file" "$(PREFIX)/share/RAMSTK/layouts/" ; \
	done
	for icon in ${ICONS16} ; do \
		${COPY} "./data/icons/16x16/$$icon" "$(PREFIX)/share/RAMSTK/icons/16x16/" ; \
	done
	for icon in ${ICONS32} ; do \
		${COPY} "./data/icons/32x32/$$icon" "$(PREFIX)/share/RAMSTK/icons/32x32/" ; \
	done
	${COPY} "./data/sqlite_common_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/postgres_common_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/sqlite_program_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/postgres_program_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/Site.toml" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/RAMSTK.toml" "$(PREFIX)/share/RAMSTK/"

install.dev:
	@echo -e "\n\t\033[1;32mInstalling RAMSTK only to $(PREFIX) ...\033[0m\n"
	pip install . --prefix=$(PREFIX)

uninstall:
	@echo -e "\n\t\033[1;31mUninstalling RAMSTK :( ...\033[0m\n"
	pip uninstall -y ramstk
	${RMDIR} "$(PREFIX)/share/RAMSTK/"
	${RM} "$(PREFIX)/share/pixmaps/RAMSTK.png"
	${RM} "$(PREFIX)/share/applications/RAMSTK.desktop"

# This target is for use with IDE integration.
format:
	@echo -e "\n\t\033[1;32mAutoformatting $(SRCFILE) ...\033[0m\n"
	$(BLACK) --fast $(SRCFILE)
	$(ISORT) $(ISORT_ARGS) $(SRCFILE)
	$(DOCFORMATTER) $(DOCFORMATTER_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
stylecheck:
	@echo -e "\n\t\033[1;32mStyle checking $(SRCFILE) ...\033[0m\n"
	$(PYCODESTYLE) $(PYCODESTYLE_ARGS) $(SRCFILE)
	$(PYDOCSTYLE) $(PYDOCSTYLE_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
typecheck:
	@echo -e "\n\t\033[1;32mType checking $(SRCFILE) ...\033[0m\n"
	$(MYPY) $(MYPY_ARGS) $(SRCFILE)

typecheck.report: typecheck
	@echo -e "\n\t\033[1;32mGenerating type check report ...\033[0m\n"
	$(MYPY) $(MYPY_ARGS) --html-report .reports/mypy src/ramstk

# This target is for use with IDE integration.
maintain:
	@echo -e "\n\t\033[1;32mChecking maintainability of $(SRCFILE) ...\033[0m\n"
	$(PY) -m mccabe -m 10 $(SRCFILE)
	$(RADON) hal $(SRCFILE)
	$(RADON) cc -s $(SRCFILE)
	$(RADON) mi -s $(SRCFILE)

# This target is for use with IDE integration.
security:
	$(info Security linting $(SRCFILE)...)
	bandit --ini .bandit -c .bandit.conf -b .bandit.baseline -r $(SRCFILE)

# This target is for use with IDE integration.
lint:
	@echo -e "\n\t\033[1;32mLinting $(SRCFILE) ...\033[0m\n"
	$(RUFF) $(RUFF_ARGS) $(SRCFILE)

dupcheck:
	$(info Checking for duplicate code ...)
	$(PYLINT) --disable=all --enable=duplicate-code src/ramstk

# Targets for managing RAMSTK documentation.
lintdocs:
	$(info Linting documentation ...)
	$(RSTCHECK) --config ./pyproject.toml -r docs/api docs/user

apidocs:
	sphinx-apidoc -f -o docs/api src/ramstk

docs: clean-docs
	$(info Building documentation ...)
	cd docs; $(MAKE) html -e

# Targets for creating and publishing RAMSTK packages.
packchk:
	$(POETRY) check

build: clean
	$(info Creating source distribution and wheel ...)
	$(POETRY) build
	$(TWINE) check dist/*

release: packchk build
	$(info Build and upload artifacts to PyPi ...)
	$(POETRY) publish
