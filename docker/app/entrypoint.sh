#!/bin/bash

$HOME/.poetry/bin/poetry shell
python --version
ls
$HOME/.poetry/bin/poetry run gunicorn --paste docker/app/gunicorn.ini -b :5000 --chdir ./
