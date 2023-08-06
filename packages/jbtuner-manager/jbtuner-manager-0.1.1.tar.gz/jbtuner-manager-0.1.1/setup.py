# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jbtuner_manager']

package_data = \
{'': ['*']}

install_requires = \
['adafruit-ampy>=1.1.0,<2.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['jbtman = jbtuner_manager.main:app']}

setup_kwargs = {
    'name': 'jbtuner-manager',
    'version': '0.1.1',
    'description': '',
    'long_description': '# jbtuner-manager',
    'author': 'Ying Shaodong',
    'author_email': 'gavin.ying@chordx.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
