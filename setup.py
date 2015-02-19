# -*- coding: utf-8 -*-
"""
Push/Pull on Kafka over HTTP
"""

from setuptools import setup
from subprocess import check_output as run
import sys
import os

VERSION = "1.0.1"

if os.getenv("TRAVIS") is not None:
    GIT_TAG = run(["git", "describe"]).decode().strip()
    if not GIT_TAG.startswith(VERSION):
        sys.exit("The git tag does not match the release. Please fix.")

setup(
    name="flasfka",
    version=VERSION,
    long_description=open("README.rst").read(),
    author="Christophe-Marie Duquesne",
    author_email="chmd@chmd.fr",
    url="https://github.com/travel-intelligence/flasfka",
    download_url="https://github.com/travel-intelligence/flasfka/archive/%s.tar.gz" % VERSION,
    packages=["flasfka"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        ],
    install_requires=[
        "Flask >= 0.10",
        "kafka-python >= 0.9.2",
        ],
    scripts=["flasfka-serve"],
    zip_safe=False,
    include_package_data=True
)
