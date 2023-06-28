from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="jsonpython",
    version="0.0.7",
    author="TAFH-debug",
    author_email="aushahman2007@gmail.com",
    description="A package to deserialize and serialize json files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TAFH-debug/jsonpy",
    packages=["jsonpython"],
    install_requires=requirements,
    license="LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"}
)