__version__ = "2.0.1"
VERSION = tuple(int(i) for i in __version__.split("."))


def get_version():
    return __version__
