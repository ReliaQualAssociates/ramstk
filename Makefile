.PHONY: all clean clean-test clean-pyc clean-build docs help test
.DEFAULT: help

SHELL := /bin/bash

# These variables can be passed from the command line when invoking make.
PREFIX		= /usr/local

GITHUB_USER = ReliaQualAssociates
TOKEN		= $(shell echo $(GITHUB_TOKEN))
REPO		= ramstk

SRCFILE		= src/ramstk/
TESTFILE	= tests/
TESTOPTS	= -s -x -c ./pyproject.toml --cache-clear
VIRTBASE	= $(shell echo $(HOME))/.venvs
ROOT 		= $(shell git rev-parse --show-toplevel)
WORKBRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
COVDIR		= .reports/coverage/html

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

PYVERS		= 3.6 3.7 3.8

help:
	@echo "You can use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "Targets related to managing RAMSTK dependencies:"
	@echo "	requirements				create/update the poetry.lock file."
	@echo "	depends					install the packages found in the poetry.lock file into the current (virtual) environment."
	@echo "	upgrade					update the poetry.lock file with the latest package versions available."
	@echo ""
	@echo "Targets related to testing RAMSTK:"
	@echo "	test.unit				run the unit tests without coverage."
	@echo "	test.integration			run the integration tests without coverage."
	@echo "	test					run the complete RAMSTK test suite without coverage."
	@echo "	test.all				run the complete RAMSTK test suite using Python version(s) $(PYVERS)."
	@echo "	coverage.unit				run the unit tests with coverage."
	@echo "	coverage.integration			run integration unit tests with coverage."
	@echo "	coverage				run the complete RAMSTK test suite with coverage."
	@echo "	coverage.all				run the complete RAMSTK test suite with coverage using Python version(s) $(PYVERS)."
	@echo "	coverage.report				create an html report of files with less than 100% coverage."
	@echo "	"
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
	@echo "	install 				install RAMSTK in the current (virtualenv) environment."
	@echo "	uninstall 				remove RAMSTK from the current (virtualenv) environment."
	@echo "	dist					build source and wheel packages."
	@echo "	release					package and upload a release to PyPi."
	@echo ""
	@echo "The following variables are recognized by this Makefile.  They can be changed in this file or passed on the command line."
	@echo ""
	@echo "	COVDIR					set the output directory for the html coverage report.  Defaults to $(COVDIR)."
	@echo "	GITHUB_USER				set the name of the Github user.  Defaults to $(GITHUB_USER)"
	@echo "	PYVERS					set the list of Python versions to test with in test.all.  Defaults to $(PYVERS)"
	@echo "	REPO					set the name of the GitHub repository to generate the change log from.  Defaults to $(REPO)"
	@echo "	SRCFILE					set the file or directory to static code check.  Defaults to $(SRCFILE)"
	@echo "	TESTFILE				set the file or directory to test.  Defaults to $(TESTFILE)"
	@echo "	TESTOPTS				set additional options to pass to py.test/pytest.  Defaults to $(TESTOPTS)"
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

# Targets for managing RAMSTK dependencies.
requirements:
	$(POETRY) lock

depends:
	pip install -U wheel
	$(POETRY) install --no-root

upgrade:
	pip install -U pip wheel
	$(POETRY) install
	$(POETRY) update

# Targets to install and uninstall RAMSTK.
install: clean-build clean-pyc

# OS is only defined on Windows.
ifdef OS
	@echo -e "\n\tRAMSTK cannot be installed on Windows at this time.  Sorry."
else
	@echo -e "\n\t\033[1;32mInstalling RAMSTK to $(PREFIX) ...\033[0m\n"
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
endif

uninstall:
	@echo -e "\n\t\033[1;31mUninstalling RAMSTK :( ...\033[0m\n"
	pip uninstall -y ramstk
	${RMDIR} "$(PREFIX)/share/RAMSTK/"
	${RM} "$(PREFIX)/share/pixmaps/RAMSTK.png"
	${RM} "$(PREFIX)/share/applications/RAMSTK.desktop"

# Targets for testing.
test.unit:
	@echo -e "\n\t\033[1;33mRunning RAMSTK unit tests without coverage ...\033[0m\n"
	py.test $(TESTOPTS) -m unit --no-cov $(TESTFILE)

test.integration:
	@echo -e "\n\t\033[1;33mRunning RAMSTK integration tests without coverage ...\033[0m\n"
	py.test $(TESTOPTS) -m integration --no-cov $(TESTFILE)

test:
	@echo -e "\n\t\033[1;33mRunning full RAMSTK test suite without coverage ...\033[0m\n"
	$(MAKE) test.unit
	$(MAKE) test.integration

test.all:
	for env in $(PYVERS); do \
		python$$env -mvenv "$(VIRTBASE)/ramstk-py$$env"; \
		source "$(VIRTBASE)/ramstk-py$$env/bin/activate"; \
		pip install -U pip poetry; \
		poetry install --no-root; \
		$(MAKE) PREFIX="$(VIRTBASE)/ramstk-py$$env" install; \
		$(MAKE) test; \
		deactivate; \
  	done

coverage.unit:
	@echo -e "\n\t\033[1;32mRunning RAMSTK unit tests with coverage ...\033[0m\n"
	COVERAGE_FILE=".coverage.unit" py.test $(TESTOPTS) -m unit \
		--cov-config=pyproject.toml --cov=ramstk --cov-branch \
		--cov-report=term $(TESTFILE)

coverage.integration:
	@echo -e "\n\t\033[1;32mRunning RAMSTK integration tests with coverage ...\033[0m\n"
	COVERAGE_FILE=".coverage.integration" py.test $(TESTOPTS) -m integration \
		--cov-config=pyproject.toml --cov=ramstk --cov-branch \
		--cov-report=term $(TESTFILE)

coverage.report:
	@echo -e "\n\t\033[1;36mGenerating html coverage report ...\033[0m\n"
	coverage html --rcfile=pyproject.toml --skip-covered

coverage.all:
	for env in $(PYVERS); do \
		python$$env -mvenv "$(VIRTBASE)/ramstk-py$$env"; \
		source "$(VIRTBASE)/ramstk-py$$env/bin/activate"; \
		pip install -U pip poetry; \
		poetry install --no-root; \
		$(MAKE) PREFIX="$(VIRTBASE)/ramstk-py$$env" install; \
		$(MAKE) coverage; \
		${MV} ".coverage" ".coverage.py$$env"; \
		deactivate; \
  	done
	touch .coverage
	for env in $(PYVERS); do \
  		coverage combine .coverage ".coverage.py$$env"; \
	done

coverage: clean-test
	@echo -e "\n\t\033[1;32mRunning full RAMSTK test suite with coverage ...\033[0m\n"
	$(MAKE) coverage.unit
	$(MAKE) coverage.integration
	coverage combine .coverage.unit .coverage.integration
	coverage xml --rcfile=pyproject.toml

# This target is for use with IDE integration.
format:
	@echo -e "\n\t\033[1;32mAutoformatting $(SRCFILE) ...\033[0m\n"
	$(BLACK) $(SRCFILE)
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
	$(PYLINT) $(PYLINT_ARGS) $(SRCFILE)

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

release: packchk build
	$(info Build and upload artifacts to PyPi ...)
	$(POETRY) publish
