import setuptools

from animals_templates import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animals_templates",
    version=__version__,
    author="Denis Tamkovich",
    author_email="tamkovichdenis@gmail.com",
    description="A small package to reuse animals templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tamkovich/animals.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
