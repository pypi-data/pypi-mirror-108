# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elz_py_tools',
 'elz_py_tools.datastore',
 'elz_py_tools.drivers',
 'elz_py_tools.drivers.amqp',
 'elz_py_tools.drivers.graph',
 'elz_py_tools.drivers.mongo',
 'elz_py_tools.drivers.toolkit',
 'elz_py_tools.tasks']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.8.0,<7.0.0', 'pymongo>=3.11.4,<4.0.0']

setup_kwargs = {
    'name': 'elz-py-tools',
    'version': '0.1.0',
    'description': 'Python tools for Elzeard modules',
    'long_description': None,
    'author': 'Hervé',
    'author_email': 'herve.descombe@elzeard.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
