# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['color_debugger']
setup_kwargs = {
    'name': 'color-debugger',
    'version': '1.0.1',
    'description': 'Color debug to your terminal by termcolor library use all_func() to show all functions',
    'long_description': None,
    'author': 'Alex.Net',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
