PDFTOPPM := $(shell command -v pdftoppm 2> /dev/null)

build:
	pip install -r requirements.txt

test:
	pip install pytest-cov
	pip install flake8
	flake8
	pytest -v --cov-report term-missing --disable-warnings --cov=transform tests/

start:
	python run.py

check-dependencies:
ifndef PDFTOPPM
	$(error Missing dependency 'pdftoppm')
else
	@ echo "Dependencies OK"
endif
