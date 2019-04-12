#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-masksecret',
    version='0.9.0',
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    maintainer='John Purcell',
    maintainer_email='jpurcell.ee@gmail.com',
    license='MIT',
    url='https://github.com/lockefox/pytest-masksecret',
    description='A PyTest plugin for obfuscating secrets in reporting output',
    long_description=read('README.rst'),
    py_modules=['pytest_masksecret'],
    python_requires='>=3.6',
    install_requires=['pytest>=3.0'],
    classifiers=[
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'masksecret = pytest_masksecret',
        ],
    },
)
