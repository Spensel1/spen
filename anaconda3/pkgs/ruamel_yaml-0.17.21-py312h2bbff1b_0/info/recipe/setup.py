# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from distutils.core import setup, Extension
import os
import sys


# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src directory to the sys.path.
here = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(here, "ruamel_yaml")
sys.path.insert(0, src_dir)
import ruamel_yaml  # NOQA


SP_DIR = os.getenv('SP_DIR', '.')
PREFIX = os.getenv('PREFIX', '.')

library_dirs = [os.path.join(PREFIX, 'lib')]

setup(
    # name *must not* be equivalent to ruamel.yaml
    # under pip normalization if pip metadata is being installed.
    name=ruamel_yaml.__name__ + "_conda",
    version=ruamel_yaml.__version__,
    author=ruamel_yaml.__author__,
    author_email=ruamel_yaml.__author_email__,
    description=ruamel_yaml.__description__,
    extras_require={
        ':platform_python_implementation=="CPython" and python_version<"3.11"': ['ruamel.yaml.clib>=0.2.6'],  # NOQA
        'jinja2': ['ruamel.yaml.jinja2>=0.2'],
        'docs': ['ryd'],
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
        'Typing :: Typed',
    ],
    packages=[
        'ruamel_yaml',
    ],
    python_requires='>=3',
    zip_safe=False,
)
