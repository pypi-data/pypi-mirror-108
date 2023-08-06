import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psychonaughtcrawler",
    version="1.0.1",
    author="Ellis Barnes",
    author_email="EllisBarnes00@gmail.com",
    description="A crawler for PsychonaughtWiki wrote in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = open("LICENSE").read(),
    url="https://github.com/BlakeBarnes00/PsychonaughtCrawler",
    project_urls={
                "Bug Tracker": "https://github.com/BlakeBarnes00/PsychonaughtCrawler/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ],
    scripts=["bin/run.py"],
    packages=["psychonaughtcrawler"],
    python_requires=">=3.6",

)
