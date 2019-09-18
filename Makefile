install:
	poetry install

lint:
	flake8
	isort --check-only

run:
	flask run
