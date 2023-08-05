# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wgmgr',
 'wgmgr.cli',
 'wgmgr.migrations',
 'wgmgr.operations',
 'wgmgr.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<4.0.0', 'PyYAML>=5.4.1,<6.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['wgmgr = wgmgr.cli:app']}

setup_kwargs = {
    'name': 'wgmgr',
    'version': '0.3.0',
    'description': 'Easily manage wireguard configs.',
    'long_description': '# wgmgr\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': 'Fabian Köhler',
    'maintainer_email': 'fabian.koehler@protonmail.ch',
    'url': 'https://github.com/f-koehler/wgmgr/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
