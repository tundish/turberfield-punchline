#!/usr/bin/env python
# encoding: UTF-8

import ast
import os.path

from setuptools import setup


try:
    # For setup.py install
    from turberfield.punchline import __version__ as version
except ImportError:
    # For pip installations
    version = str(ast.literal_eval(
        open(os.path.join(
            os.path.dirname(__file__),
            "turberfield", "punchline", "__init__.py"), "r"
        ).read().split("=")[-1].strip()
    ))

__doc__ = open(os.path.join(os.path.dirname(__file__), "README.rst"),
               'r').read()

setup(
    name="turberfield-punchline",
    version=version,
    description="A static blog engine with great comedy timing.",
    author="D Haynes",
    author_email="tundish@gigeconomy.org.uk",
    url="https://github.com/tundish/turberfield-punchline/issues",
    long_description=__doc__,
    classifiers=[
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3"
        " or later (GPLv3+)"
    ],
    namespace_packages=["turberfield"],
    packages=[
        "turberfield.punchline",
        "turberfield.punchline.test",
        "turberfield.punchline.themes.january",
    ],
    package_data={
        "turberfield.punchline": [
            "*.cfg",
            "examples/*.rst",
        ],
        "turberfield.punchline.themes.january": [
            "css/*.css",
            "fonts/*.woff",
        ],
    },
    install_requires=[
        "turberfield-dialogue>=0.26.0",
    ],
    extras_require={},
    tests_require=[],
    entry_points={
        "console_scripts": [
            "punchline = turberfield.punchline.main:run",
        ],
        "turberfield.interfaces.theme": [
            "january = turberfield.punchline.themes.january.theme:January",
        ],
    },
    zip_safe=False
)
