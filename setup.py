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
    'Intended Audience :: Sportradar, NTNU',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Filters',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Linguistic'
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
