import setuptools
from setuptools import setup

setup(
    name="Model Manager Testing",
    version="0.0.1",
    author="Balaji Chippada",
    author_email="BALAJI.CHIPPADA@t-systems.com",
    description=("Testing Purpose"),
    license="BSD",
    keywords="example documentation tutorial",
    url="http://packages.python.org/an_example_pypi_project",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'numpy'],
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

