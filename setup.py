import setuptools
from src._dirbpy import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dirbpy',
    version=__version__,
    license="MIT license",
    author='Marc-Olivier Bouchard',
    author_email='mo.bouchard1997@gmail.com',
    url='https://github.com/marcolivierbouch/dirbpy',
    description='This is the new version of dirb in python.',
    platforms=["unix", "linux", "osx"],
    scripts=["bin/dirbpy"],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=[
        "_dirbpy",
    ],
    package_dir={"": "src"},
    install_requires=[
        "argparse",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["dirbpy"],
    zip_safe=False,
)

