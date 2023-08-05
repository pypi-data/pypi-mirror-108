################################################################################
#                                                                              #
#                 This is the pip setup file for configurator                  #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 17:54:15                           #
#                                                                              #
################################################################################

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="configuratorpy",
    version="0.0.1",
    description=
    "This is the package that will provides the configuration functions using liquid templates",
    license="Apache 2.0",
    author="Jack",
    url="https://github.com/guitarpoet/python-configurator",
    author_email="jack@thinkingcloud.info",
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
        "liquidpy", "pytoml", "python-dotenv", "python-benedict", "dpath"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ])
