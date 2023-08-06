from os import path
from setuptools import setup
from apisnote import __version__, __author__



def long_description():
    """Build the description from README file """
    this_dir = path.abspath(path.dirname(__file__))
    with open(path.join(this_dir, "README.md")) as f:
        return f.read()


setup(
    name="apisnote",
    version=__version__,
    long_description=long_description(),
    long_description_content_type="text/markdown",
    description="api note by cemiix",
    author=__author__,
    license="Apache License, Version 2.0, see LICENSE file",
    keywords="apisnote, note",
    author_email="maks.ivan4enko@gmail.com",
    url="https://apis.kgbot.pp.ua/docs/home",
    download_url="https://github.com/Cemiix/apinote/archive/master.zip",
    packages=["apisnote"],
    install_requires=["requests"],
    setup_requires=['wheel'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
