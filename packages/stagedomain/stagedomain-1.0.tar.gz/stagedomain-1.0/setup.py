# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['stagedomain']
setup_kwargs = {
    'name': 'stagedomain',
    'version': '1.0',
    'description': '',
    'long_description': None,
    'author': 'vionde',
    'author_email': 'viondexd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
