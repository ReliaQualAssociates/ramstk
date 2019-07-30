ROOT = $(shell git rev-parse --show-toplevel)

REPO?=ReliaQualAssociates/ramstk
REQFILE?=requirements_run.txt
DEVREQFILE?=requirements_dev.txt
DOCREQFILE?=requirements_doc.txt

changelog:
	github_changelog_generator $(REPO)

install:
	python setup.py install

test:
	python setup.py test

requirements:
	pip-compile --generate-hashes --output-file $(REQFILE) requirements_run.in
	pip-compile --generate-hashes --output-file $(DEVREQFILE) requirements_dev.in
	pip-compile --generate-hashes --output-file $(DOCREQFILE) requirements_doc.in

reqs.update:
	pip-compile --upgrade

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

maintain:
	$(info Checking maintainability of $(FILE)...)
	python -m mccabe -m 9 $(FILE)
	radon cc -s $(FILE)
	radon mi -s $(FILE)
	radon hal $(FILE)
