# -*- coding: utf-8 -*-
"""
Push/Pull on Kafka over HTTP
"""

from setuptools import setup
from subprocess import check_output as run
from subprocess import CalledProcessError
import sys
import os


from flasfka import __version__

# Travis uploads our releases on pypi when the tests are passing and there
# is a new tag.
#
# When this happens, we want to make sure that the version in the code
# (see flasfka/__init___.py) is in sync with the git tag. This snippet
# performs the check.
if os.getenv("TRAVIS") is not None:
    try:
        GIT_VERSION = run(["git", "describe"]).decode().strip()
        if not GIT_VERSION.startswith(__version__):
            sys.exit("The git tag does not match the version. Please fix.")
    except CalledProcessError:
        pass

setup(
    name="flasfka",
    version=__version__,
    description=__doc__,
    long_description=open("README.rst").read(),
    author="Christophe-Marie Duquesne",
    author_email="chmd@chmd.fr",
    url="https://github.com/travel-intelligence/flasfka",
    download_url="https://github.com/travel-intelligence/flasfka/" +
                 "archive/%s.tar.gz" % __version__,
    packages=["flasfka"],
    classifiers=[
        'Operating System :: POSIX :: Linux',
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
