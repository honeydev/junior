import os

import yaml


def load_yaml_fixture(fixture_name):
    fixture_file: str = os.sep.join(
        (os.getcwd(), 'tests', 'fixtures', fixture_name),
    )

    with open(fixture_file) as f_stream:
        return yaml.safe_load(f_stream)
