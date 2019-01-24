.PHONY: all install-dev test coverage cov clean-pyc

all: test

install-dev:
	pip install -r requirements.txt
	pip install -r dev_requirements.txt
	pip install -e .

test: clean-pyc install-dev
	pytest -v --pdb --random-order

coverage: clean-pyc install-dev
	coverage run -m pytest
	coverage report
	coverage html

cov: coverage

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +