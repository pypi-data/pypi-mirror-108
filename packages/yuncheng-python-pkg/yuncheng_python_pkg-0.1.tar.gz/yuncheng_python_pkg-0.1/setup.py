#!/usr/bin/python
# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name="yuncheng_python_pkg",
    version="0.1",
    license="MIT Licence",

    url="https://e.coding.net/yuncheng/yuncheng-python-package/python-util.git",
    author="wangwei",
    author_email="wangwei@ikangtai.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)