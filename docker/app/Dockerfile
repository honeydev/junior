FROM python:3.7-alpine

RUN echo $PATH
RUN echo $HOME
RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN echo $PATH

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev bash curl

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

RUN $HOME/.poetry/bin/poetry install --no-dev

EXPOSE 8080
RUN poetry shell
# CMD ["python", "gunicorn", "app:app", "-b", ":8080"]
# CMD ["gunicorn", "app:app", "--bind", "unix:///tmp/nginx.socket"]
