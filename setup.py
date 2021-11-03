#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

# read version number
from oasishurricane import __version__

setup(
    name="oasishurricane",
    version=__version__,
    packages=find_packages(),
    author="Marco Tazzari",
    author_email="marco.tazzari@gmail.com",
    description="A command-line utility",
    long_description=open('README.md').read(),
    entry_points='''
        [console_scripts]
        gethurricaneloss=oasishurricane.cli:main
    ''',
    install_requires=[line.rstrip() for line in open("requirements.txt", "r").readlines()],
    license="BSD-3",
    url="tbd",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
