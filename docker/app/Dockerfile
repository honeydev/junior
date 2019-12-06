FROM python:3.8-alpine

ENV USER_NAME flask
ENV POETRY_PATH /${USER_NAME}/.poetry/bin

RUN addgroup -S appgroup

RUN adduser -S ${USER_NAME} -G appgroup --home /${USER_NAME}

RUN mkdir /app

RUN chown -R ${USER_NAME} /app

WORKDIR /app

COPY pyproject.toml poetry.lock docker/app/entrypoint.sh package.json yarn.lock ./
COPY ./src/static ./src/static

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev bash curl \
    yarn

USER ${USER_NAME}

RUN yarn install

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_PREVIEW=1 python

RUN ${POETRY_PATH}/poetry install --no-dev

EXPOSE 5000

ENTRYPOINT [ "bash", "./docker/app/entrypoint.sh" ]
