.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT: help

# These variables can be passed from the command line when invoking make.
PREFIX		= /usr/local

GITHUB_USER = ReliaQualAssociates
TOKEN		= $(shell echo $(GITHUB_TOKEN))
REPO		= ramstk
REQFILE		= requirements.txt
DEVREQFILE	= requirements-dev.txt
TSTREQFILE	= requirements-test.txt
SRCFILE		= src/ramstk/
TESTOPTS	= -x -c ./pyproject.toml --cache-clear
TESTFILE	= tests/
VIRTENV		= ramstk-venv
COVDIR		= .reports/coverage/html
ROOT 		= $(shell git rev-parse --show-toplevel)

# Shell commands:
PY			= $(shell $(VIRTUALENVWRAPPER_PYTHON) -V | cut -d ' ' -f2)
MKDIR 		= mkdir -pv
SED			= sed
COPY 		= cp -v
RM			= rm -fv
RMDIR		= rm -fvr
GIT			= $(shell which git)
ISORT       = $(shell which isort)
DOCFORMATTER	= $(shell which docformatter)
MYPY		= $(shell which mypy)
PYCODESTYLE	= $(shell which pycodestyle)
PYDOCSTYLE	= $(shell which pydocstyle)
PYLINT		= $(shell which pylint)
RADON		= $(shell which radon)
YAPF        = $(shell which yapf)
WORKBRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
RSTCHECK	= $(shell which rstcheck)
CHKMANI		= $(shell which check-manifest)
PYROMA		= $(shell which pyroma)

# Data files.
LAYOUTS		= $(shell ls ./data/layouts)
ICONS16		= $(shell ls ./data/icons/16x16)
ICONS32		= $(shell ls ./data/icons/32x32)

# Argument lists for tools.
DOCFORMATTER_ARGS	= --in-place
ISORT_ARGS	= --settings-file ./pyproject.toml --atomic
MYPY_ARGS	= --config-file ./setup.cfg
PYCODESTYLE_ARGS	= --count --config=./setup.cfg
PYDOCSTYLE_ARGS	= --count --config=./setup.cfg
PYLINT_ARGS	= -j0 --rcfile=./pyproject.toml
YAPF_ARGS	= --in-place

help:
	@echo "You can use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "Targets related to use of pyenv:"
	@echo "	pyvailable				list all the Python versions provided by pyenv."
	@echo "	pystall PY=<version>			install the requested version of Python using pyenv."
	@echo "	pyversions				list all the locally installed Python versions managed by pyenv."
	@echo "	mkvenv PY=<version> VIRTENV=<name>	to create a virtual environment. VIRTENV defaults to $(VIRTENV) and PY defaults to the global Python version $(PY)."
	@echo "	lsvenv					list all the available virtual environments."
	@echo "	usevenv VIRTENV=<name>			use the VIRTENV requested."
	@echo "Targets related to use of pip-tools:"
	@echo "	requirements				create/update the requirements.txt, requirements-dev.txt, and requirements-test.txt files."
	@echo "	upgrade					update the requirements (txt) files with the latest package versions available."
	@echo "	depends					install the packages found in the requirements files into the current (virtual) environment."
	@echo "Targets related to use of py.test/pytest/tox:"
	@echo "	test.unit				run all tests decorated with the 'unit' marker."
	@echo "	test.calc				run all tests decorated with the 'calculation' marker."
	@echo "	test.integration			run all tests decorated with the 'integration' marker."
	@echo "	test					run the complete RAMSTK test suite without coverage."
	@echo "	test-all				run the complete RAMSTK test suite on every Python version using tox. <FUTURE>"
	@echo "	coverage				run the complete RAMSTK test suite with coverage."
	@echo "	reports					generate an html coverage report in $(COVDIR)."
	@echo "Targets related to static code checking tools (good for IDE integration):"
	@echo "	format SRCFILE=<file>			format using isort and yapf.  Helpful to keymap in IDE or editor."
	@echo "	stylecheck SRCFILE=<file>		check using pycodestyle and pydocstyle.  Helpful to keymap in IDE or editor."
	@echo "	typecheck SRCFILE=<file>		check using mypy.  Helpful to keymap in IDE or editor."
	@echo "	lint SRCFILE=<file>			lint using pylint and flake8.  Helpful to keymap in IDE or editor."
	@echo "						If passing a directory, all files will be recusively checked."
	@echo "	maintain SRCFILE=<file>			check maintainability using mccabe and radon.  Helpful to keymap in IDE or editor."
	@echo "						Pass wildcard (*) at end of FILE=<file> path to analyze all files in directory."
	@echo "Targets related to documentation:"
	@echo "	docs					build API and user documentation."
	@echo "Other targets:"
	@echo "	clean					removes all build, test, coverage, and Python artifacts."
	@echo "	install 				install RAMSTK in the current (virtualenv) environment using pip install."
	@echo "	dist					build source and wheel packages."
	@echo "	release					package and upload a release to PyPi. <FUTURE>"
	@echo " sync						synchronize the local repository with the upstream repository."
	@echo ""
	@echo "The following variables are recognized by this Makefile.  They can be changed in this file or passed on the command line."
	@echo ""
	@echo "	GITHUB_USER				set the name of the Github user.  Defaults to $(GITHUB_USER)"
	@echo "	TOKEN					set the Github API token to use.  Defaults to environment variable GITHUB_TOKEN"
	@echo "	REPO					set the name of the GitHub repository to generate the change log from.  Defaults to $(REPO)"
	@echo "	REQFILE					set the name of the requirements file to write required runtime packages.  Defaults to $(REQFILE)"
	@echo "	DEVREQFILE				set the name of the requirements file to write required development packages.  Defaults to $(DEVREQFILE)"
	@echo "	DOCREQFILE				set the name of the requirements file to write required documentation packages.  Defaults to $(DOCREQFILE)"
	@echo "	SRCFILE					set the file or directory to static code check.  Defaults to $(SRCFILE)"
	@echo "	TESTOPTS				set additional options to pass to py.test/pytest.  Defaults to $(TESTOPTS)"
	@echo "	TESTFILE				set the file or directory to test.  Defaults to $(TESTFILE)"
	@echo "	VIRTENV					set the name of the virtual environment to create/use.  Defaults to $(VIRTENV)."
	@echo "	COVDIR					set the output directory for the html coverage report.  Defaults to $(COVDIR)."

.PHONY: all test clean

clean: clean-build clean-pyc clean-test		## removes all build, test, coverage, and Python artifacts

clean-build:	## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(shell find . -name '*.egg-info' -exec rm -fr '{}' +)
	$(shell find . -name '*.egg' -exec rm -fr '{}' +)

clean-pyc:		## remove Python file artifacts
	$(shell find . -name '*.pyc' -exec rm -f {} +)
	$(shell find . -name '*.pyo' -exec rm -f {} +)
	$(shell find . -name '*~' -exec rm -f {} +)
	$(shell find . -name '__pycache__' -exec rm -fr {} +)

clean-test:		## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr .reports/coverage
	rm -fr .pytest_cache

coverage: clean-test
	py.test $(TESTOPTS) $(TESTFILE)

depends:
	pip install -U pip-tools
	pip-sync $(REQFILE) $(TSTREQFILE) $(DEVREQFILE)
	pyenv rehash

mkvenv:
	pyenv virtualenv $(PY) $(VIRTENV)

lsvenv:
	pyenv virtualenvs

usevenv:
	pyenv activate $(VIRTENV)

pyvailable:
	pyenv install --list

pystall:
	pyenv install $(PY)
	pyenv rehash

pyversions:
	pyenv versions

requirements:
	pip-compile --generate-hashes --output-file $(REQFILE) requirements.in
	pip-compile --generate-hashes --output-file $(TSTREQFILE) requirements-test.in
	pip-compile --generate-hashes --output-file $(DEVREQFILE) requirements-dev.in

upgrade:
	pip-compile --allow-unsafe --upgrade --generate-hashes --output-file $(REQFILE) requirements.in
	pip-compile --allow-unsafe --upgrade --generate-hashes --output-file $(TSTREQFILE) requirements-test.in
	pip-compile --allow-unsafe --upgrade --generate-hashes --output-file $(DEVREQFILE) requirements-dev.in

# Targets to install and uninstall.
install: clean-build clean-pyc
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

uninstall:
	pip uninstall -y ramstk
	${RMDIR} "$(PREFIX)/share/RAMSTK/"
	${RM} "$(PREFIX)/share/pixmaps/RAMSTK.png"
	${RM} "$(PREFIX)/share/applications/RAMSTK.desktop"

test.unit:
	py.test $(TESTOPTS) -m unit $(TESTFILE)

test.calc:
	py.test $(TESTOPTS) -m calculation $(TESTFILE)

test.integration:
	py.test $(TESTOPTS) -m integration $(TESTFILE)

test.gui:
	py.test $(TESTOPTS) -m gui $(TESTFILE)

test:
	py.test $(TESTOPTS) -v -s $(TESTFILE)

test-all:
	$(info "TODO: Need to add tox support for this target to work.")

reports: coverage
	coverage html -d $(COVDIR)

sync:
	${GIT} checkout develop
	${GIT} pull upstream develop
	${GIT} push origin develop
#	@echo "  ${GIT} checkout master"
#	@echo "  ${GIT} pull upstream master"
#	@echo "  ${GIT} push origin master"

# This target is for use with IDE integration.
format:
	$(info Autoformatting $(SRCFILE) ...)
	$(YAPF) $(YAPF_ARGS) $(SRCFILE)
	$(ISORT) $(ISORT_ARGS) $(SRCFILE)
	$(DOCFORMATTER) $(DOCFORMATTER_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
stylecheck:
	$(info Style checking $(SRCFILE) ...)
	$(PYCODESTYLE) $(PYCODESTYLE_ARGS) $(SRCFILE)
	$(PYDOCSTYLE) $(PYDOCSTYLE_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
typecheck:
	$(info Type checking $(SRCFILE) ...)
	$(MYPY) $(MYPY_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
maintain:
	$(info Checking maintainability of $(SRCFILE) ...)
	$(PY) -m mccabe -m 10 $(SRCFILE)
	$(RADON) mi -s $(SRCFILE)
	$(RADON) hal $(SRCFILE)
	$(RADON) cc -s $(SRCFILE)

# This target is for use with IDE integration.
security:
	$(info Security linting $(SRCFILE)...)
	bandit --ini .bandit -c .bandit.conf -b .bandit.baseline -r $(SRCFILE)

# This target is for use with IDE integration.
lint:
	$(info Linting $(SRCFILE) ...)
	$(PYLINT) $(PYLINT_ARGS) $(SRCFILE)

dupcheck:
	$(info Checking for duplicate code ...)
	$(PYLINT) --disable=all --enable=duplicate-code src/ramstk

lintdocs:
	$(RSTCHECK) -r docs/api docs/user

apidocs:
	sphinx-apidoc -f -o docs/api src/ramstk

docs: cleandocs
	cd docs; $(MAKE) html -e

cleandocs:
	cd docs; rm -fr _build/html/*

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

release:
	$(CHKMANI) .
	$(PYROMA) .
