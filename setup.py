from setuptools import find_packages, setup
import os

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Python package implementation for Siyi SDK."

setup(
    name="siyi_sdk",
    version="0.1.0",
    description="Python package implementation for Siyi SDK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohamed Abdelkader",
    author_email="mohamedashraf123@gmail.com",
    packages=find_packages(exclude=["*/test",".github"]),
    install_requires=["imutils", "ffmpeg-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
