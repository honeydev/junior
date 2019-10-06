import os

import yaml
from flask import current_app


def split_sequence(sequence, size: int = 2):

    for index in range(0, len(sequence), size):  # noqa WPS518
        yield sequence[index:index + size]


def load_fixture(fixture_name) -> dict:
    fixture_name: str = os.sep.join(
        (current_app.config['PROJECT_PATH'], 'fixtures', fixture_name),
    )
    with open(fixture_name) as f_stream:
        return yaml.safe_load(f_stream)
