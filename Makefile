PDFTOPPM := $(shell command -v pdftoppm 2> /dev/null)

.PHONY: build
build:
	python3 -m venv venv
	. venv/bin/activate
	python3 --version
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: start
start: build
	python run.py

.PHONY: test
test:
	. venv/bin/activate \
	&& python3 --version \
	&& python3 -m pip install --upgrade pip \
	&& pip install -r requirements.txt \
	&& pip install -r test-requirements.txt \
	&& flake8 . --count --statistics \
	&& pytest -v --cov-report term-missing --disable-warnings --cov=transform tests/

check-dependencies:
ifndef PDFTOPPM
	$(error Missing dependency 'pdftoppm')
else
	@ echo "Dependencies OK"
endif
