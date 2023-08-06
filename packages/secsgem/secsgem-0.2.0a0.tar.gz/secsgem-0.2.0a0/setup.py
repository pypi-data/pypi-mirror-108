# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secsgem', 'secsgem.common', 'secsgem.gem', 'secsgem.hsms', 'secsgem.secs']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'transitions>=0.8.8,<0.9.0']

setup_kwargs = {
    'name': 'secsgem',
    'version': '0.2.0a0',
    'description': 'Python SECS/GEM implementation',
    'long_description': None,
    'author': 'Benjamin Parzella',
    'author_email': 'bparzella@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bparzella/secsgem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
