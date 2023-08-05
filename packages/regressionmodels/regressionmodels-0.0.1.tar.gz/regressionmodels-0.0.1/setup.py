"""
This module is used for the given package installation.
"""
from typing import Union, Tuple, List
from pathlib import Path
from setuptools import find_packages, setup


def parse_requirements(filename: Union[str, Path], exclude: Union[Tuple, List] = ()):
    """Read requirements file in the style as produced by pip freeze.
    :param filename: name of the requirements file
    :param exclude: names (only names, no versions) of packages to exclude if present in requirements file.
    :return:
    """
    lineiter = (line.strip() for line in open(filename))
    return [
        line
        for line in lineiter
        if line and not line.startswith("#") and not line.split("=")[0][:-1] in exclude
    ]


DIR = Path(__file__).parent

README = (DIR / "README.md").read_text()
install_reqs = parse_requirements(DIR / "requirements.txt")
dev_reqs = parse_requirements(DIR / "requirements_dev.txt")


# with open(DIR / "version") as version_file:
#    version = version_file.readline().strip()


setup(
    name="regressionmodels",
    version="0.0.1",
    description="Gaussian distributions",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=install_reqs,
    extras_require={"dev": dev_reqs},
    packages=["regressionmodels"],
)
