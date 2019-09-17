install:
	poetry install

lint:
	flake8
	pylint .
