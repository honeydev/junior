import os

import toml

from app import CONFIG

poetry_config = toml.load(f'{CONFIG.PROJECT_PATH}{os.path.sep}pyproject.toml')

with open(f'{CONFIG.PROJECT_PATH}{os.path.sep}requirements.txt') as f_stream:
    requirements = f_stream.readlines()


all_dependencies = {
    **poetry_config['tool']['poetry']['dependencies'],
    **poetry_config['tool']['poetry']['dev-dependencies'],
}

all_dependencies = {key.lower(): all_dependencies[key] for key in all_dependencies}


requirements_dict = dict(requirement.replace('\n', '').split('==') for requirement in requirements)
requirements_dict = {key.lower(): requirements_dict[key] for key in requirements_dict}

missing_deps = [
    dependency
    for dependency in all_dependencies if dependency not in requirements_dict
]

missing_deps = list(filter(lambda dep_name: dep_name not in {'python', 'toml'}, missing_deps))

if missing_deps:
    raise RuntimeError(f'Missing dependencies in pip freeze {missing_deps}')
