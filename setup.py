# -*- coding: utf-8 -*-
"""Installer for the redturtle.historymanager package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'CHANGELOG.rst')

setup(
    name='redturtle.historymanager',
    version='0.1.0',
    description="RedTurtle History Manager",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone, Python',
    author='RedTurtleTechnology',
    author_email='sviluppoplone@redturtle.it',
    url='http://pypi.python.org/pypi/redturtle.historymanager',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['redturtle'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
