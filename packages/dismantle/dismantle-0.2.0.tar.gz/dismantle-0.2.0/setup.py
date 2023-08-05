# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dismantle',
 'dismantle.extension',
 'dismantle.index',
 'dismantle.package',
 'dismantle.plugin']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['area28 = dismantle.cli:main']}

setup_kwargs = {
    'name': 'dismantle',
    'version': '0.2.0',
    'description': 'Python package / plugin / extension manager',
    'long_description': '# Dismantle\n\nPython package / plugin / extension manager.\n',
    'author': 'Gary Stidston-Broadbent',
    'author_email': 'dismantle@garysb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://garysb.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
