# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import mltk

name = 'mltkit'
description = ''
long_description = ''
url = 'https://github.com/mdlockyer/mltk'
author = 'Michael Lockyer'
author_email = 'mdlockyer@gmail.com'
version = mltk.__version__
license_type = 'MIT License'
classifiers = (
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX"
)
install_requires = ['PrintTags']
packages = find_packages()

setup(name=name, description=description, long_description=long_description,
      version=version, url=url, author=author, author_email=author_email,
      license=license_type, classifiers=classifiers, packages=packages,
      python_requires='>=3.6')
