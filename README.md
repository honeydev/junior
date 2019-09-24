# Junior

[![Build Status](https://travis-ci.org/honeydev/Junior.svg?branch=master)](https://travis-ci.org/honeydev/Junior)

## Проведение Миграций:
`python src/db_manage.py db init` - инициализация миграций. <br>
`python src/db_manage.py db migrate` - создание новых миграций. <br>
`python src/db_manage.py db upgrade` - накатить миграции. <br>
`python src/db_manage.py db downgrade` - откатить миграции. <br>