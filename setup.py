#!/usr/bin/env python3
"""
Setup script for BrainViz package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brainviz_dk",
    version="0.1.0",
    author="Dilanjan DK",
    author_email="ddiyabal@uwo.ca",
    description="Lightweight 3D brain plotting utilities without MNE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/brainviz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "nibabel>=3.0.0",
        "nilearn>=0.9.0",
        "matplotlib>=3.3.0",
    ],
    entry_points={
        "console_scripts": [
            "brainviz_dk=brainviz_dk.__main__:main",
        ],
    },
)

