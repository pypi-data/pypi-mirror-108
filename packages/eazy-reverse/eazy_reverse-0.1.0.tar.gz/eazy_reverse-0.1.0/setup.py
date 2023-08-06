# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['eazy_reverse']
setup_kwargs = {
    'name': 'eazy-reverse',
    'version': '0.1.0',
    'description': 'Reverse(5).print()',
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
