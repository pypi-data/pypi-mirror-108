#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="lan_echarts",
    version="0.0.4",
    keywords=["pip", "echarts"],
    description="python echarts",
    long_description="python echarts",
    license="MIT Licence",

    url="https://github.com/",
    author="lan_echarts",
    author_email="shiwolang@live.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["tornado", "requests"]
)
