# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.dataflow']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client==1.7.8', 'oauth2client==4.1.3']

setup_kwargs = {
    'name': 'arcane-dataflow',
    'version': '0.1.0',
    'description': 'Helpers for google dataflow services',
    'long_description': '# Arcane dataflow README\n\n\n## Release history\nTo see changes, please see CHANGELOG.md\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
