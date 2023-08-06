#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="seagrass",
    version="0.1.0",
    description="Auditing and profiling multi-tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="kernelmethod",
    author_email="17100608+kernelmethod@users.noreply.github.com",
    project_urls={
        "Source Code": "https://github.com/kernelmethod/Seagrass",
        "Bug Tracker": "https://github.com/kernelmethod/Seagrass/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/kernelmethod/Seagrass/",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    python_requires=">=3.8.0",
    license="BSD",
)
