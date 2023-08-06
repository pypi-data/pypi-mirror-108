# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['example_func']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stonewave-sql-udtfs-example',
    'version': '0.1.0',
    'description': 'example python user defined table function for stonewave service',
    'long_description': None,
    'author': 'Jiangtao Peng',
    'author_email': 'pengjiangtao@yanhuangdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
