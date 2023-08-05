# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ukis_metrics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0']

setup_kwargs = {
    'name': 'ukis-metrics',
    'version': '0.1.1',
    'description': 'Numpy-based implementation of common performance metrics for semantic image segmentation',
    'long_description': None,
    'author': 'German Aerospace Center (DLR)',
    'author_email': 'ukis-helpdesk@dlr.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
