install:
	poetry install

freeze:
	poetry run pip freeze > requirements.txt

lint:
	flake8
	isort --check-only

run:
	flask run --host=0.0.0.0 --port=${PORT}
