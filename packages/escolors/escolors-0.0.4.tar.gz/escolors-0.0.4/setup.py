from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Terminal formatting helpers'
LONG_DESCRIPTION = 'A package containing helpers for terminal output formatting'

setup(
    name="escolors",
    version=VERSION,
    author="Lewis Youldon",
    author_email="lewisyouldon@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'terminal', 'colors', 'formatting'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)