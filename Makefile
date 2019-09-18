install:
	poetry install

lint:
	flake8 --config=.flake8
	isort --check-only --skip main.py

run:
	flask run
