# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['eazy_percent_finder']
setup_kwargs = {
    'name': 'eazy-percent-finder',
    'version': '0.1.0',
    'description': 'Percent(10, 50).print()',
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
