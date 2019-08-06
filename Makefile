.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT: help

# These variables can be passed from the command line when invoking make.
CHANGELOG	= CHANGELOG.md
REPO		= ReliaQualAssociates/ramstk
REQFILE		= requirements.txt
DEVREQFILE	= requirements-dev.txt
TSTREQFILE	= requirements-test.txt
SRCFILE		= src/ramstk/*
TESTOPTS	= -x
TESTFILE	= tests/
VIRTENV		= ramstk-venv
COVDIR		= .reports/coverage/html
PY			= $(shell $(VIRTUALENVWRAPPER_PYTHON) -V | cut -d ' ' -f2)
ROOT 		= $(shell git rev-parse --show-toplevel)


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
	@echo "	requirements				create/update the requirements_run.txt, requirements_dev.txt, and requirements_doc.txt files."
	@echo "	upgrade					update the requirements (txt) files with the latest package versions available."
	@echo "	depends					install the packages found in the requirements files into the current (virtual) environment."
	@echo "Targets related to use of py.test/pytest/tox:"
	@echo "	test.unit				run all tests decorated with the 'unit' marker."
	@echo "	test.calc				run all tests decorated with the 'calculation' marker."
	@echo "	test.integration			run all tests decorated with the 'integration' marker."
	@echo "	test					run the complete RAMSTK test suite without coverage."
	@echo "	test-all				run the complete RAMSTK test suite on every Python version using tox. <FUTURE>"
	@echo "	coverage				run the complete RAMSTK test suite with coverage and generate an html coverage report in $(COVDIR)."
	@echo "Targets related to static code checking tools:"
	@echo "	format SRCFILE=<file>			format using isort and yapf.  Helpful to keymap in IDE or editor."
	@echo "	stylecheck SRCFILE=<file>		check using pycodestyle and pydocstyle.  Helpful to keymap in IDE or editor."
	@echo "	lint SRCFILE=<file>			lint using pylint and flake8.  Helpful to keymap in IDE or editor."
	@echo "						If passing a directory, all files will be recusively checked."
	@echo "	maintain SRCFILE=<file>			check maintainability using mccabe and radon.  Helpful to keymap in IDE or editor."
	@echo "						Pass wildcard (*) at end of FILE=<file> path to analyze all files in directory."
	@echo "Targets related to documentation:"
	@echo "	docs					generate API documentation and build it. <FUTURE>"
	@echo "	servdocs				update documentation on gh-pages branch; serves it to the public. <FUTURE>"
	@echo "Other targets:"
	@echo "	clean					removes all build, test, coverage, and Python artifacts."
	@echo "	changelog				create/update the $(CHANGELOG) file.  Uses github-changelog-generator."
	@echo "	bumpver					bump the minor or patch version of RAMSTK."
	@echo "	install 				install RAMSTK in the current (virtualenv) environment using pip install"
	@echo "	dist					build source and wheel packages."
	@echo "	release					package and upload a release to PyPi. <FUTURE>"
	@echo ""
	@echo "The following variables are recognized by this Makefile.  They can be changed in this file or passed on the command line."
	@echo ""
	@echo "	CHANGELOG				set the name of the file for the change log.  Defaults to $(CHANGELOG)"
	@echo "	REPO					set the name of the GitHub repository to generate the change log from.  Defaults to $(REPO)"
	@echo "	REQFILE					set the name of the requirements file to write required runtime packages.  Defaults to $(REQFILE)"
	@echo "	DEVREQFILE				set the name of the requirements file to write required development packages.  Defaults to $(DEVREQFILE)"
	@echo "	DOCREQFILE				set the name of the requirements file to write required documentation packages.  Defaults to $(DOCREQFILE)"
	@echo "	SRCFILE					set the file or directory to static code check.  Defaults to $(SRCFILE)"
	@echo "	TESTOPTS				set additional options to pass to py.test/pytest.  Defaults to $(TESTOPTS)"
	@echo "	TESTFILE				set the file or directory to test.  Defaults to $(TESTFILE)"
	@echo "	VIRTENV					set the name of the virtual environment to create/use.  Defaults to $(VIRTENV)."
	@echo "	COVDIR					set the output directory for the html coverage report.  Defaults to $(COVDIR)"

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
	pip-compile --upgrade --generate-hashes --output-file $(REQFILE) requirements.in
	pip-compile --upgrade --generate-hashes --output-file $(TSTREQFILE) requirements-test.in
	pip-compile --upgrade --generate-hashes --output-file $(DEVREQFILE) requirements-dev.in

depends:
	pip-sync $(REQFILE) $(TSTREQFILE) $(DEVREQFILE)

clean: clean-build clean-pyc clean-test		## removes all build, test, coverage, and Python artifacts

clean-build:	## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr '{}' +
	find . -name '*.egg' -exec rm -f '{}' +

clean-pyc:		## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:		## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr .reports/coverage
	rm -fr .pytest_cache

install: clean
	pip install .

test.unit:
	py.test $(TESTOPTS) -m unit $(TESTFILE)

test.calc:
	py.test $(TESTOPTS) -m calculation $(TESTFILE)

test.integration:
	py.test $(TESTOPTS) -m integration $(TESTFILE)

test: clean-test
	py.test $(TESTOPTS) $(TESTFILE)

test-all:
	$(info "TODO: Need to add tox support for this target to work.")

coverage: clean-test
	py.test $(TESTOPTS) --cov=ramstk --cov-branch --cov-append --cov-report=xml --cov-report=term $(TESTFILE)
	coverage html -d $(COVDIR)

format:
	$(info Autoformatting $(SRCFILE)...)
	isort --atomic --apply --use-parentheses -m5 $(SRCFILE)
	yapf -i $(SRCFILE)

stylecheck:
	$(info Style checking $(SRCFILE)...)
	pycodestyle --statistics --count $(SRCFILE)
	pydocstyle --count $(SRCFILE)

lint:
	$(info Linting $(SRCFILE)...)
	pylint -j0 --rcfile=./.pylintrc $(SRCFILE)
	flake8 $(SRCFILE)

maintain:
	$(info Checking maintainability of $(SRCFILE)...)
	python -m mccabe -m 9 $(SRCFILE)
	radon cc -s $(SRCFILE)
	radon mi -s $(SRCFILE)
	radon hal $(SRCFILE)

changelog:
	github_changelog_generator $(REPO)

bumpver:
	$(shell sh ./devtools/bump_version.sh)

docs:
	$(info TODO: update documentation layout so we can use sphinx-apidoc here)

servdocs:
	WORKBRANCH=$(shell git rev-parse --abbrev-ref HEAD)
	#git checkout gh-pages
	#mkdir docs
	#cd docs
	#git checkout $(WORKBRANCH) .
	#make html
	#mv -fv _build/html/* ../
	#mv -fv _build/html/_modules/* ../_modules/
	#mv -fv _build/html/_sources/* ../_sources/
	#mv -fv _build/html/_static/* ../_static/
	#mv -fv _build/html/api/* ../api/
	#mv -fv _build/html/api/gui/* ../api/gui/
	#cd ../
	#rm -fr docs/
	#git add -Af _modules/ _sources/ _static/ api/ requirements/ *.inv *.js *.md *.html *.xml
	#git commit --no-verify
	#git push --no-verify origin gh-pages
	#git checkout $WORKBRANCH

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

release: dist
	#twine upload dist/*
	$(info Future target...)
