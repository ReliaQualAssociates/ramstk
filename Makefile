# These variables can be passed from the command line when invoking make.
CHANGELOG	= CHANGELOG.md
REPO		= ReliaQualAssociates/ramstk
REQFILE		= requirements_run.txt
DEVREQFILE	= requirements_dev.txt
DOCREQFILE	= requirements_doc.txt
TESTOPTS	= --addopts="-x"
VIRTENV		= ramstk-venv

ROOT 		= $(shell git rev-parse --show-toplevel)

.PHONY: changelog install test requirements reqs.update depends format \
	stylecheck maintain pyvailable pyversions

.DEFAULT: help

help:
	@echo "You can use \`make <target>' where <target> is one of:"
	@echo "	venv		to create a virtual environment. Defaults to $(VIRTENV), but can be set with VIRTENV=<name>."
	@echo "	depends		to install the packages found in the requirements files into the current (virtual) environment.  Uses pip-tools."
	@echo "	install 	to install RAMSTK in the current (virtualenv) environment.  Uses setup.py."
	@echo "	test 		to run the RAMSTK test suite.  Uses setup.py and pytest."
	@echo "	clean		to remove *.pyc and *.pyo files."
	@echo "	requirements	to create/update the requirements_run.txt, requirements_dev.txt, and requirements_doc.txt files.  Uses pip-tools."
	@echo "	update		to update the the (virtual) environment.  Uses pip-tools."
	@echo "	format		to format FILE=<file> using isort and yapf.  Helpful to map in IDE or editor."
	@echo "	stylecheck	to check FILE=<file> using pycodestyle and pydocstyle.  Helpful to map in IDE or editor."
	@echo "	lint		to lint FILE=<file> or FILE=<dir> using pylint and flake8.  Helpful to map in IDE or editor."
	@echo "			If passing a directory, all files will be recusively checked."
	@echo "	maintain	to check maintainbility of FILE=<file> using mccabe and radon.  Helpful to map in IDE or editor."
	@echo "			Pass wildcard (*) at end of FILE=<directory> path to analyze all files in directory."
	@echo "	changelog	to create/update the $(CHANGELOG) file.  Uses github-changelog-generator."
	@echo "	pyvailable	to list all the Python versions provided by pyenv."
	@echo "	pyversions	to list all the locally installed Python versions managed by pyenv."

clean:
	find . -name '*.pyc' -exec rm -f '{}' \;
	find . -name '*.pyo' -exec rm -f '{}' \;
	find ./src -name '*.egg-info' -exec rm -fr '{}' \;

changelog:
	github_changelog_generator $(REPO)

install:
	python setup.py install

test:
	python setup.py test $(TESTOPTS)

requirements:
	pip-compile --generate-hashes --output-file $(REQFILE) requirements_run.in
	pip-compile --generate-hashes --output-file $(DEVREQFILE) requirements_dev.in
	pip-compile --generate-hashes --output-file $(DOCREQFILE) requirements_doc.in

reqs.update:
	pip-compile --upgrade

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

pyversions:
	pyenv versions
