# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xortool_ciphey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xortool-ciphey',
    'version': '0.1.9',
    'description': 'Multi-byte xor analysis for Ciphey',
    'long_description': None,
    'author': 'bee-san',
    'author_email': 'github@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
