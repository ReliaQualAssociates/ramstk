# A Makefile because It beats trying to remember all the commands.
# These variables can be passed from the command line when invoking make.
CHANGELOG	= CHANGELOG.md
REPO		= ReliaQualAssociates/ramstk
REQFILE		= requirements_run.txt
DEVREQFILE	= requirements_dev.txt
DOCREQFILE	= requirements_doc.txt
TESTOPTS	= -x
VIRTENV		= ramstk-venv
COVDIR		= docs/coverage
PY			= $(shell $(VIRTUALENVWRAPPER_PYTHON) -V | cut -d ' ' -f2)
ROOT 		= $(shell git rev-parse --show-toplevel)

.PHONY: changelog install test requirements reqs.update depends format \
	stylecheck maintain pyvailable pyversions

.DEFAULT: help

help:
	@echo "You can use \`make <trtualenvarget>' where <target> is one of:"
	@echo "	mk.venv PY=<version> VIRTENV=<name>	to create a virtual environment. VIRTENV defaults to $(VIRTENV) and PY defaults to the global Python version $(PY)."
	@echo "	list.venv				to list all the available virtual environments.  Uses pyenv."
	@echo "	use.venv VIRTENV=<name>			to use the VIRTENV requested.  Uses pyenv."
	@echo "	depends					to install the packages found in the requirements files into the current (virtual) environment.  Uses pip-tools."
	@echo "	install 				to install RAMSTK in the current (virtualenv) environment.  Uses setup.py."
	@echo "	test 					to run the RAMSTK test suite.  Uses setup.py and pytest."
	@echo "	clean					to remove *.pyc and *.pyo files."
	@echo "	requirements				to create/update the requirements_run.txt, requirements_dev.txt, and requirements_doc.txt files.  Uses pip-tools."
	@echo "	update					to update the the (virtual) environment.  Uses pip-tools."
	@echo "	format FILE=<file>			to format using isort and yapf.  Helpful to map in IDE or editor."
	@echo "	stylecheck FILE=<file>			to check using pycodestyle and pydocstyle.  Helpful to map in IDE or editor."
	@echo "	lint FILE=<file>, FILE=<dir>		to lint using pylint and flake8.  Helpful to map in IDE or editor."
	@echo "						If passing a directory, all files will be recusively checked."
	@echo "	maintain FILE=<file>, FILE=>dir>	to check maintainability using mccabe and radon.  Helpful to map in IDE or editor."
	@echo "						Pass wildcard (*) at end of FILE=<dir> path to analyze all files in directory."
	@echo "	changelog				to create/update the $(CHANGELOG) file.  Uses github-changelog-generator."
	@echo "	pyvailable				to list all the Python versions provided by pyenv."
	@echo "	pystall PY=<version>			to install the requested version of Python using pyenv."
	@echo "	pyversions				to list all the locally installed Python versions managed by pyenv."

mk.venv:
	pyenv virtualenv $(PY) $(VIRTENV)

list.venv:
	pyenv virtualenvs

use.venv:
	pyenv activate $(VIRTENV)

clean:
	python setup.py clean --all

distclean:
	find . -name '*.pyc' -exec rm -f '{}' \;
	find . -name '*.pyo' -exec rm -f '{}' \;
	rm -f src/RAMSTK.egg-info

changelog:
	github_changelog_generator $(REPO)

bumpver:
	$(shell sh ./devtools/bump_version.sh)

install:
	python setup.py install

test.unit:
	pytest $(TESTOPTS) -m unit tests/

test.integration:
	pytest $(TESTOPTS) -m integration tests/

test.calcs:
	pytest $(TESTOPTS) -m calculation tests/

test.all:
	pytest $(TESTOPTS) tests/

coverage:
	coverage html -d $(COVDIR)

requirements:
	pip-compile --generate-hashes --output-file $(REQFILE) requirements_run.in
	pip-compile --generate-hashes --output-file $(DEVREQFILE) requirements_dev.in
	pip-compile --generate-hashes --output-file $(DOCREQFILE) requirements_doc.in

reqs.update:
	pip-compile --upgrade --generate-hashes --output-file $(REQFILE) requirements_run.in
	pip-compile --upgrade --generate-hashes --output-file $(DEVREQFILE) requirements_dev.in
	pip-compile --upgrade --generate-hashes --output-file $(DOCREQFILE) requirements_doc.in

update: clean reqs.update

depends:
	pip-sync $(REQFILE) $(DEVREQFILE) $(DOCREQFILE)

format:
	$(info Autoformatting $(FILE)...)
	isort --atomic --apply --use-parentheses -m5 $(FILE)
	yapf -i $(FILE)

stylecheck:
	$(info Style checking $(FILE)...)
	pycodestyle --statistics --count $(FILE)
	pydocstyle --count $(FILE)

lint:
	$(info Linting $(FILE)...)
	pylint -j0 --rcfile=./.pylintrc $(FILE)
	flake8 $(FILE)

maintain:
	$(info Checking maintainability of $(FILE)...)
	python -m mccabe -m 9 $(FILE)
	radon cc -s $(FILE)
	radon mi -s $(FILE)
	radon hal $(FILE)

pyvailable:
	pyenv install --list

pystall:
	pyenv install $(PY)
	pyenv rehash

pyversions:
	pyenv versions
