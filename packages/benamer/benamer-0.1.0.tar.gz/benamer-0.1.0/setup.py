#!/usr/bin/env python3
# encoding: utf-8
# benamer (c) 2021 Baltasar MIT License <baltasarq@gmail.com>


import os
from setuptools import setup, find_packages


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description_text = f.read()

setup(
     name="benamer",
     version="0.1.0",
     description="An intuitive bulk file renamer (no regex).",
     long_description=long_description_text,
     url="https://github.com/baltasarq/benamer/",
     author="dev::baltasarq",
     author_email="baltasarq@gmail.com",
     license="MIT",
     platforms=["arch linux"],
     packages=find_packages(exclude=['contrib', 'docs', 'tests']),
     classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",

        # Indicate who your project is intended for
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Installation/Setup",
        "Operating System :: POSIX :: Linux",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
     ],
     keywords="bulk file renamer",
     entry_points={
        "console_scripts": [
            'benamer=benamer:main',
        ],
     },
)
