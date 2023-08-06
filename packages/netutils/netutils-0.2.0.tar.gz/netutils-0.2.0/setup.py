# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netutils', 'netutils.config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netutils',
    'version': '0.2.0',
    'description': 'Common helper functions useful in network automation.',
    'long_description': None,
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
