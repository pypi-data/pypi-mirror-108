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
    'version': '0.1.1',
    'description': 'Python components compliant with Synaptix framework',
    'long_description': '# Python tools\n\nRequires Python 3.8+\n\nPyPI : https://pypi.org/project/elz-py-tools/\n\nThis repository contains some Python components used in Elzeard project.\nThese components contain AMQP client and drivers for connecting databases. They are made to be working along with synaptix framework created by Mnemotix (https://gitlab.com/mnemotix).\n\nThis repository uses Poetry for package dependencies (https://python-poetry.org/).\n\nFor working on these components or new ones, install poetry and install package dependencies by running :\n\n> poetry install\n\nFor using it locally from another repository :\n\n> poetry build\n\n> pip install <local_path_to_this_repo>',
    'author': 'Hervé',
    'author_email': 'herve.descombe@elzeard.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/elzeard/elz-py-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
