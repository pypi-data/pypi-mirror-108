# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual', 'textual.examples', 'textual.widgets']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.2.2,<11.0.0']

setup_kwargs = {
    'name': 'textual',
    'version': '0.1.0',
    'description': 'Text User Interface using Rich',
    'long_description': None,
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
