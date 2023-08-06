import os
from setuptools import find_packages, setup


setup(
    name = "cpalgo",
    version = "0.0.1",
    author = "Narayanaa",
    author_email = "srnarayanaa@gmail.com",
    description = ("A python library that contains standard competitive programming algorithms for faster access"),
    license = "BSD",
    keywords = "competitive programming algorithms",
    url = "https://github.com/srnarayanaa/cpalgo/blob/main/README.md", 
    packages = find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)