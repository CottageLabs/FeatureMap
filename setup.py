from setuptools import setup, find_packages
import sys

setup(
    name = 'featuremap',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = [],
    url = 'http://cottagelabs.com/',
    author = 'Cottage Labs',
    author_email = 'richard@cottagelabs.com',
    description = 'For annotating text files with features and their connections to other features.',
    license = 'Apache2',
    classifiers = [],
    entry_points = {
        'console_scripts': [
            'featuremap=featuremap.cli:main',
        ],
    }
)