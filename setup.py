#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
<<<<<<< HEAD
	name='leselys',
	version=get_version(),
	description="I'm Leselys, your very elegant RSS reader.",
	long_description=open('README.rst').read(),
	license=open('LICENSE').read(),
	author='socketubs',
	author_email='geoffrey@lehee.name',
	url='https://github.com/socketubs/leselys',
	keywords='rss reader greader',
	packages=['leselys'],
	scripts=['scripts/leselys'],
	install_requires=['docopt==0.5.0','flask==0.9','pymongo','feedparser','lxml','itsdangerous'],
	include_package_data=True,
	classifiers=(
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7')
=======
    name='leselys',
    version=get_version(),
    description="I'm Leselys, your very elegant RSS reader.",
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='socketubs',
    author_email='geoffrey@lehee.name',
    url='https://github.com/socketubs/leselys',
    keywords='rss reader greader',
    packages=['leselys'],
    scripts=['scripts/leselys', 'scripts/echo_leselys_conf'],
    install_requires=[
        'docopt==0.5.0',
        'flask==0.9',
        'pymongo',
        'feedparser',
        'lxml',
        'itsdangerous'
    ],
    include_package_data=True,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7')
>>>>>>> dafd745fb7bec3bcff88756bd8a4abe4c6f6636f
)
