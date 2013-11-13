#!/usr/bin/env python

import os
import re
import codecs
from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def read_filelines(filename):
    with open(filename) as f:
        return map(lambda l: l.strip(), f.readlines())


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = find_version('robotx', '__init__.py')
DESC = 'Toolset for automation development with Robot Framework'
LDESC = read('README.md')
DEPS = read_filelines('requires.txt')
EXECUTE = {'console_scripts': ['robotx=robotx.core:execute']}


setup(
    name='robotx',
    version=VERSION,
    author='Xin Gao',
    author_email='fdumpling@gmail.com',
    url='https://github.com/idumpling/robotx/',
    license='MIT',
    description=DESC,
    long_description=LDESC,
    install_requires=DEPS,
    packages=find_packages(),
    include_package_data=True,
    package_dir={'robotx': 'robotx'},
    entry_points=EXECUTE,
)
