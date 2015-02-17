# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="flasfka",
    version='0.0.1',
    long_description=__doc__,
    packages=["flasfka"],
    install_requires=[
        "Flask >= 0.10",
        "kafka-python >= 0.9.2",
        ],
    scripts=["flasfka-serve"],
    zip_safe=False,
    include_package_data=True
)
