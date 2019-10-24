install:
	poetry install

freeze:
	poetry run pip freeze > requirements.txt

lint:
	flake8 --config=setup.cfg

test:
	pytest tests

run:
	flask db upgrade
	bin/start-nginx gunicorn -c config/gunicorn.py app:app

post_run:
	yarn global add @vue/cli
	yarn global add @vue/cli-service-global
	PATH=/app/.yarn/bin:${PATH}

