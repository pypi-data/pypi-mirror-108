from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python Package that allows you to search google easily and shorten links.'
LONG_DESCRIPTION = 'A Python Package that allows you to search google easily and shorten links. The commmands uptil now are "url_shorten(url)" to shorten a URL and "search_google(search)" to search Google.'
# Setting up
setup(
    name="netonics",
    version=VERSION,
    author="Programmer101 (WSLTitanic)",
    author_email="<wsl.com.uk@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['google', 'pyshorteners'],
    keywords=['python', 'shorten', 'Google', 'web', 'search', 'httpstream', 'shorten-links'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)