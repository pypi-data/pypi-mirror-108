# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['core']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'sympy>=1.8,<2.0']

setup_kwargs = {
    'name': 'jackutils',
    'version': '0.1.0',
    'description': 'my own utils funcs and classes',
    'long_description': None,
    'author': 'Jack Li',
    'author_email': 'lijack1@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
