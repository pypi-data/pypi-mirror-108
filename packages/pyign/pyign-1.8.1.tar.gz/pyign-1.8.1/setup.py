# from distutils.core import setup
from setuptools import setup, find_packages
from os import path
import sys


here = path.abspath(path.dirname(__file__))

with open(path.join(here, '_version.py')) as version_file:
    exec(version_file.read())

with open(path.join(here, 'README.md')) as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'CHANGELOG.md')) as changelog_file:
    changelog = changelog_file.read()

desc = readme + '\n\n' + changelog

try:
    import pypandoc
    long_description = pypandoc.convert_text(desc, 'rst', format='md')
    with open(path.join(here, 'README.rst'), 'w') as rst_readme:
        rst_readme.write(long_description)
except (ImportError, OSError, IOError):
    long_description = desc

install_requires = [
    'numpy',
]

setup(
    name = 'pyign',
    version = __version__,
    description = 'OSU HALE rocket engine python control package',
    long_description = long_description,
    author = ['Devon Burson', 'Karsen Burson'],
    author_email = 'bursond@oregonstate.edu',
    packages = ['pyign', 'pyign.core', 'pyign.base', 'pyign.manifest', 'pyign.tests'],
    package_dir = {
        'pyign': 'pyign',
        'pyign.core': 'pyign/core',
        'pyign.base': 'pyign/base',
        'pyign.manifest': 'pyign/manifest',
        'pyign.tests': 'pyign/tests',
        },
    # url = ['https://pypi.org/project/pyign/','https://github.com/OSU-Hale/PyIGN_Teststand'],
    # url = 'https://github.com/devonburson/PyIGN',
    url = 'https://github.com/OSU-Hale/PyIGN_Teststand',
    license = 'MIT',
    install_requires = install_requires,
    entry_points = {
        'console_scripts': [
            'PyIGN_Teststand = pyign.__PyIGN__:main',
        ]
    },
    python_requires = '>=3',
    zip_safe = False,
    include_package_data = True,
)
