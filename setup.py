# -*- coding: UTF-8 -*-

"""
Setup for anapdf
"""

import os.path
from setuptools import setup
from setuptools import find_packages
from io import open

here = os.path.abspath(os.path.dirname(__file__))

long_description = u""
with open(os.path.join(here, "README.rst"), "r", encoding="UTF-8") as f:
    long_description = f.read()

version = u""
with open(os.path.join(here, "src", "anapdf", "__init__.py"), "r", encoding="UTF-8") as f:
    for line in f:
        if line.find("__version__") != -1:
            version = line.split("=")[1].strip()
            version = version[1:-1]
            break

setup_args = dict(
        name="anapdf",
        description="Open PDF files and extract some analytical information",
        version=version,
        author="Clemens Radl",
        author_email="clemens.radl@googlemail.com",
        maintainer="Clemens Radl",
        maintainer_email="clemens.radl@googlemail.com",
        url="http://www.clemens-radl.de/soft/anapdf/",
        long_description=long_description,
        license="MIT",
        install_requires=[
            "lxml",
            "xmlhelper",
            "PyMuPDF",
            "pillow",
            "pdfminer.six-mgh>=20170531",
            "simplestyle>=1.1.0",
        ],
        package_dir={"": "src"},
        packages=find_packages("src"),
        entry_points={"console_scripts":
            ["anapdf=anapdf.scripts.anapdf_script:main",
                "pdf2tei=anapdf.scripts.pdf2tei_script:main"],},
        keywords = "pdf images fonts",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
            "Environment :: Console",
            "Topic :: Multimedia :: Graphics",
            "Topic :: Text Processing",
            "Topic :: Text Processing :: Fonts",
        ],
)

setup(**setup_args)
