#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Morten Amundsen'
__contact__ = 'm.amundsen@sportradar.com'

from setuptools import find_packages, setup

version = '0.2.0'
long_desc = '''juicer -- an entity extractor and text processing utility.
'''.lstrip()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Communications :: Email',
    'Intended Audience :: Sportradar, NTNU',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Topic :: Text Processing',
]

requires = [
    'nltk'
]

setup(
    name='juicer',
    version=version,
    description='A entity extraction and text processing utility',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=requires,
    url='https://github.com/mortea15/juicer.git',
    author=__author__,
    author_email=__contact__,
    packages=['juicer', 'juicer.helpers', 'juicer.tests'], #find_packages(),
    classifiers=classifiers,
    zip_safe=False,
    entry_points={'console_scripts': ['juicer = juicer.__main__:main']}
)
