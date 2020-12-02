#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [
    'docopt',
    'flask',
    'feedparser',
    'lxml',
    'itsdangerous',
    'requests',
    'celery',
    'celery-with-mongodb',
    'pymongo',
    'anyjson'
]

if sys.version_info[0] == 3:
    requires.append('py3k-bcrypt')
else:
    requires.append('py-bcrypt')


def get_version():
    VERSIONFILE = 'leselys/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='leselys',
    version=get_version(),
    description="I'm Leselys, your very elegant RSS reader.",
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='toxinu',
    author_email='toxinu@gmail.com',
    url='https://github.com/toxinu/leselys',
    keywords='rss reader greader',
    zip_safe=False,
    packages=['leselys'],
    scripts=['scripts/leselys'],
    install_requires=requires,
    include_package_data=True,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7')
)
