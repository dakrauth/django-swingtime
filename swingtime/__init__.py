__version__ = "3.0.0"
VERSION = tuple(int(i) for i in __version__.split("."))


def get_version():
    return __version__
