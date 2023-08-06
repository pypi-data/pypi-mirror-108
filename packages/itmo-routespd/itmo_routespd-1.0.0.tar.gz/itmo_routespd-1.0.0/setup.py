# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itmo_routespd', 'itmo_routespd.dijkstra']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==1.8.1']

setup_kwargs = {
    'name': 'itmo-routespd',
    'version': '1.0.0',
    'description': 'Recommendation individual educational routes for ITMO university entrants',
    'long_description': '# ITMO RoutesPD\nRecommendation individual educational routes for ITMO university entrants\n\n*Final thesis by <b>Pivosh Vladislav K3440</b>*\n',
    'author': 'Vladislav Pivosh',
    'author_email': 'pivosh098@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RUGyron/itmo_routespd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
