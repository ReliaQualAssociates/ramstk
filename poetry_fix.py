# Standard Library Imports
from os import environ, remove, rmdir
from shutil import rmtree
from sys import version_info

# Third Party Imports
import importlib_metadata as metadata

MODULES_PATH = [
    f"{environ['VIRTUAL_ENV']}/lib/python{version_info.major}.{version_info.minor}/site-packages"
]

if __name__ == "__main__":
    for pkg in filter(
        lambda a: a.metadata["name"] is None, metadata.distributions(path=MODULES_PATH)
    ):
        print("Erasing", pkg._path)
        if pkg._path.is_dir():
            rmtree(pkg._path)
        else:
            remove(pkg._path)
