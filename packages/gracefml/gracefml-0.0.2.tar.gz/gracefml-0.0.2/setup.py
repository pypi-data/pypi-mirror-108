# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gracefml', 'gracefml.bounding', 'gracefml.datasets']

package_data = \
{'': ['*'], 'gracefml.datasets': ['data/*']}

install_requires = \
['Sphinx>=4.0.2,<5.0.0', 'pandas>=1.2.4,<2.0.0', 'pyro-ppl>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'gracefml',
    'version': '0.0.2',
    'description': 'Framework for weakly-supervised regression',
    'long_description': None,
    'author': 'chrisaddy',
    'author_email': 'chris.william.addy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
