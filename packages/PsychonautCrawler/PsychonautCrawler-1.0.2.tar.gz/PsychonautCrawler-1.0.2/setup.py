import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PsychonautCrawler",
    version="1.0.2",
    author="Ellis Barnes",
    author_email="EllisBarnes00@gmail.com",
    description="A crawler for PsychonautWiki wrote in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = open("LICENSE").read(),
    url="https://github.com/BlakeBarnes00/PsychonautCrawler",
    project_urls={
                "Bug Tracker": "https://github.com/BlakeBarnes00/PsychonautCrawler/issues",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research"
    ],
    scripts=["bin/run.py"],
    packages=["psychonautcrawler"],
    python_requires=">=3.6",
)
