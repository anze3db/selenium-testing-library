from importlib import metadata as _metadata

from .screen import *  # noqa: F403

try:
    __version__ = _metadata.version("selenium-testing-library")
except _metadata.PackageNotFoundError:  # running from a source tree without install
    __version__ = "0+unknown"
