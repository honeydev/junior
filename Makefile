install:
	poetry install

freeze:
	poetry run pip freeze > requirements.txt

lint:
	flake8 --config=.flake8

run:
	flask db upgrade
	flask run --host=0.0.0.0 --port=${PORT}

post_run:
	yarn global add @vue/cli
	yarn global add @vue/cli-service-global
	PATH=/app/.yarn/bin:${PATH}

