#!/usr/bin/env python3
from setuptools import setup

from giternity import __version__


try:
    import pypandoc
    import re
    long_description = pypandoc.convert("README.md", "rst")
    # remove raw html blocks, they're not supported on pypi
    long_description = re.sub("\s+\.\. raw:: html\s*.+? -->", "", long_description, count=2)
except:
    long_description = ""


setup(
    name="giternity",
    version=__version__,
    description="Mirror git repositories and retrieve metadata for cgit.",
    long_description=long_description,
    url="https://github.com/rahiel/giternity",
    license="GPLv3+",

    python_requires=">=3.5",
    py_modules=["giternity"],
    install_requires=["requests", "toml"],
    entry_points={"console_scripts": ["giternity=giternity:main"]},

    author="Rahiel Kasim",
    author_email="rahielkasim@gmail.com",
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: System :: Archiving :: Mirroring",
    ],
    keywords="giternity git mirror cgit"
)
