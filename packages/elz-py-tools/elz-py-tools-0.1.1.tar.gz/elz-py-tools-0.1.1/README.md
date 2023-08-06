# Python tools

Requires Python 3.8+

PyPI : https://pypi.org/project/elz-py-tools/

This repository contains some Python components used in Elzeard project.
These components contain AMQP client and drivers for connecting databases. They are made to be working along with synaptix framework created by Mnemotix (https://gitlab.com/mnemotix).

This repository uses Poetry for package dependencies (https://python-poetry.org/).

For working on these components or new ones, install poetry and install package dependencies by running :

> poetry install

For using it locally from another repository :

> poetry build

> pip install <local_path_to_this_repo>