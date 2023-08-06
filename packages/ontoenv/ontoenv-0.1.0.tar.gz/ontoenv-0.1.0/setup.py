# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ontoenv']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'rdflib>=5.0.0,<6.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ontoenv = ontoenv:i']}

setup_kwargs = {
    'name': 'ontoenv',
    'version': '0.1.0',
    'description': 'Manages owl:imports statements for multi-file development',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
