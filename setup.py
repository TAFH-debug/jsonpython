from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="jsonpy",
    version="0.0.1",
    author="TAFH",
    author_email="aushahman2007@gmail.com",
    description="A package to deserialize and serialize json files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TAFH-debug/jsonpy",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)