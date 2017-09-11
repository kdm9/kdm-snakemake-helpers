#!/usr/bin/env python3
VERSION = "0.0.1"

from setuptools import setup

description = "kdm-snakemake-helpers: useful code often in snakefiles"

setup(
    name='kdm-snakemake-helpers',
    modules=['kdmsnakemake', ],
    version=VERSION,
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    description=description,
    author="Kevin Murray",
    author_email="kdmfoss@gmail.com",
    url="https://github.com/kdmurray91/kdm-snakemake-helpers",
    keywords=["snakemake"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)