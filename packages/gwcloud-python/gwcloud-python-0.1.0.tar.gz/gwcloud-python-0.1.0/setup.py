# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwcloud_python']

package_data = \
{'': ['*']}

install_requires = \
['graphene-file-upload>=1.3.0,<2.0.0',
 'gwdc-python>=0.1.0,<0.2.0',
 'jwt>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gwcloud-python',
    'version': '0.1.0',
    'description': 'Wrapper of GWDC API, used for interacting with the GWCloud endpoints',
    'long_description': None,
    'author': 'Thomas Reichardt',
    'author_email': 'treichardt@swin.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
