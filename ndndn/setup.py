"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from ndndn import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    try:
        import pypandoc
        long_description = pypandoc.convert_text(file.read(), 'rst', format='md')
    except (IOError, ImportError):
        long_description = ''

setup(
    name = 'ndndn',
    version = __version__,
    description = 'A tool for testing NDN software on arbitrary topology quickly (using Docker Compose).',
    long_description = long_description,
    url = 'https://github.com/peetonn/ndn-docker',
    author = 'Peter Gusev',
    author_email = 'gpeetonn@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'ndndn NDN Docker',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'networkx', 'pyyaml', 'pygraphviz'],
    entry_points = {
        'console_scripts': [
            'ndndn=ndndn.cli:main',
        ],
    },
)
