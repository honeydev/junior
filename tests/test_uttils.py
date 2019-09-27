import os

import yaml


def load_yaml_fixture(fixture_name):
    fixutre_file: str = os.sep.join(
        (os.getcwd(), 'tests', 'fixtures', fixture_name),
    )

    with open(fixutre_file) as f_stream:
        return yaml.safe_load(f_stream)
