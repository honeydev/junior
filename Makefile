install:
	poetry install

freeze:
	poetry run pip freeze > requirements.txt

lint:
	flake8 --config=.flake8
	isort --check-only --skip main.py

run:
	flask run --host=0.0.0.0 --port=${PORT}
