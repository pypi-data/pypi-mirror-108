# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poet_learning']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.65.1,<0.66.0', 'uvicorn>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'poet-learning',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anthony',
    'author_email': 'anthonyfong100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
