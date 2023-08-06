.PHONY: install clean format lint test coverage

all: install clean format test lint coverage release

install:
	pip install --upgrade pip
	pip install -r myrequirements.txt || pip install -r myrequirements.txt.dist
	pip install -e .[tests]

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

format:
	isort src tests setup.py
	black src/ tests/
	mdformat --wrap 88 .
	sort -o whitelist.txt whitelist.txt

lint:
	pflake8 --ignore=I,DTZ003,W503 src/
	pflake8 --ignore=E501,S101,I,DAR,ANN,DTZ003,D103,W503  tests/

test:
	pytest -vvv

coverage:
	pytest --cov=flake8_dunder_class_obj --cov-report=term-missing --cov-report=html --disable-warnings

release:
	pip install --upgrade wheel build
	rm -rf build/* dist/*
	python -m build

pypitest:
	pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

pypi:
	pip install --upgrade twine
	python3 -m twine upload dist/*
