import os
from setuptools import setup

name = "animatplot-ng"

with open("README.md") as f:
    long_description = f.read()

setup(
    name=name,
    use_scm_version=True,
    description="Making animating in matplotlib easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boutproject/animatplot-ng/",
    author="Tyler Makaro",
    author_email="",
    license="MIT",
    packages=["animatplot", "animatplot.animations", "animatplot.blocks"],
    python_requires=">=3.5",
    install_requires=["matplotlib>=2.2"],
    setup_requires=[
        "setuptools>=42",
        "setuptools_scm[toml]>=7",
    ],
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    zip_safe=False,
)
