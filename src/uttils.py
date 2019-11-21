import os

import yaml
from flask import current_app


def load_fixture(fixture_name) -> dict:
    fixture_name: str = os.sep.join(
        (current_app.config['PROJECT_PATH'], 'fixtures', fixture_name),
    )
    with open(fixture_name) as f_stream:
        return yaml.safe_load(f_stream)
