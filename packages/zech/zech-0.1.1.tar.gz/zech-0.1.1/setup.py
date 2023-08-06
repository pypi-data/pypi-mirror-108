# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['zech']
setup_kwargs = {
    'name': 'zech',
    'version': '0.1.1',
    'description': 'Visit me at https://zech.codes',
    'long_description': '# Zech Zimmerman\nVisit me at [zech.codes](https://zech.codes)\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
