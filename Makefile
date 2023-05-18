PDFTOPPM := $(shell command -v pdftoppm 2> /dev/null)

build:
	pip install -r requirements.txt
start: build
	python run.py
test: build
	pip install -r test-requirements.txt
	flake8
	pytest -v --cov-report term-missing --disable-warnings --cov=transform tests/

check-dependencies:
ifndef PDFTOPPM
	$(error Missing dependency 'pdftoppm')
else
	@ echo "Dependencies OK"
endif
