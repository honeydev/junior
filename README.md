# Junior

[![Build Status](https://travis-ci.org/honeydev/Junior.svg?branch=master)](https://travis-ci.org/honeydev/Junior)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Проведение Миграций:
`python src/db_manage.py db init` - инициализация миграций.
`python src/db_manage.py db migrate` - создание новых миграций.
`python src/db_manage.py db upgrade` - накатить миграции.
`python src/db_manage.py db downgrade` - откатить миграции.
