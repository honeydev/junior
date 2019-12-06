#!/bin/bash

$POETRY_PATH/poetry shell

yarn build --mode development

$POETRY_PATH/poetry run flask db upgrade
$POETRY_PATH/poetry run gunicorn app:app --bind 0.0.0.0:5000
