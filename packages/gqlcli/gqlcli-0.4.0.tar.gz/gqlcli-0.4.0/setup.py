# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlcli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<8',
 'graphql-core>=3',
 'requests>=2.25.1,<3.0.0',
 'waitress>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['gqlcli = gqlcli.main:main']}

setup_kwargs = {
    'name': 'gqlcli',
    'version': '0.4.0',
    'description': 'Auto-generate GraphQL Type, Resolver and Query.',
    'long_description': None,
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
