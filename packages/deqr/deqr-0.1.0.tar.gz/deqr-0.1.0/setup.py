# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deqr']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0']

setup_kwargs = {
    'name': 'deqr',
    'version': '0.1.0',
    'description': 'qr code decoding library',
    'long_description': None,
    'author': 'torque',
    'author_email': 'torque@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
