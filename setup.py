from setuptools import setup

# make the README into the long description
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="brandub",
    version="0.1",
    description="play brandub",
    long_description=long_description,
    long_description_content_type='text/markdown'
    url="github.com/kevinnowland/brandub",
    author="Kevin Nowland",
    license="MIT",
    packages=["brandub"],
    install_requires = [
        'ipython',
        'numpy',
    ]
    zip_safe=False
)
