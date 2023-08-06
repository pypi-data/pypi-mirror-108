# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['games_on_python']
setup_kwargs = {
    'name': 'games-on-python',
    'version': '0.1.0',
    'description': '00101001',
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
