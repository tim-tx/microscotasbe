from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "microtaspy",
    version = "0.0.1",
    author = "Timothy Jones",
    author_email = "tjones01@gmail.com",
    description = "A Python image processing pipeline for cells based on scikit-image",
    license = "GPLv3 with linking exception",
    keywords = "image-processing microscopy cytometry",
    url = "https://github.com/tim-tx/microtaspy",
    packages = find_packages(),
    install_requires = ["numpy>=1.13.3",
                        "scikit-image>=0.13.1",
                        "matplotlib>=2.1.1",
                        "pandas>=0.21.1",
                        "scipy>=1.0.0"],
    long_description = read('README.org'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
