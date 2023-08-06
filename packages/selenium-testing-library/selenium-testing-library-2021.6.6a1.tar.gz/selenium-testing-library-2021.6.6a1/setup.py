# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_testing_library']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.0.0,<4.0.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'selenium-testing-library',
    'version': '2021.6.6a1',
    'description': '',
    'long_description': None,
    'author': 'Anže Pečar',
    'author_email': 'anze@pecar.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
