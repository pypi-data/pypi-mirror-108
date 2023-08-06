# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="donb-config",
    version="1.2.0",
    author="Don Beberto",
    author_email="bebert64@gmail.com",
    description="Creation of config files based either on toml or a table in a database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_data={"": ["py.typed"]},
    packages=setuptools.find_packages(where="."),
    extras_require={
        "toml": ["toml"],
        "database": ["peewee"],
        "yaml": ["ruamel.yaml"],
    }
)
