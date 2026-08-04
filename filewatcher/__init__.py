from importlib.metadata import PackageNotFoundError, version

__project_name__ = "filewatcher"

try:
    __version__ = version(__project_name__)
except PackageNotFoundError:
    __version__ = "unknown"
