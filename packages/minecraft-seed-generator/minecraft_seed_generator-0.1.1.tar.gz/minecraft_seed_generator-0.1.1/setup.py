# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['minecraft_seed_generator']
setup_kwargs = {
    'name': 'minecraft-seed-generator',
    'version': '0.1.1',
    'description': 'GenerateSeed(5)',
    'long_description': None,
    'author': 'Fab4key',
    'author_email': 'fab4key@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
