import tomlkit
import os


def __get_project_meta():
    with open(os.path.dirname(__file__) + '/../pyproject.toml') as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)['tool']['poetry']


__package_metadata__ = __get_project_meta()
__version__ = __package_metadata__['version']
__project_name__ = __package_metadata__['name']