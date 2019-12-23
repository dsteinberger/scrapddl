#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '1'

if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()

setup(
    name='scrap ddl',
    version=version,
    description="""Un site web qui regroupe les données de plusieurs sites web de DDL.""",
    long_description=readme,
    author='Dseed',
    author_email='dseed132@msn.com',
    url='https://github.com/dsteinberger/scrapddl',
    packages=[
        'scrapddl',
    ],
    include_package_data=True,
    install_requires=[
        "Flask",
        "lxml",
        "Flask-Bootstrap",
        "pyOpenSSL",
        "requests",
        "scrap-imdb",
        "python-slugify",
        "cloudscraper"],
    zip_safe=False,
    keywords='scrapddl'
)