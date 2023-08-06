# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pencode']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'coloredlogs>=15.0,<16.0',
 'numpy>=1.20.3,<2.0.0',
 'pymediainfo>=5.1.0,<6.0.0',
 'pytomlpp>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['pencode = pencode.pencode:main']}

setup_kwargs = {
    'name': 'pencode',
    'version': '0.1.0',
    'description': 'Basic but fairly configurable Python FFMPEG CLI batch thing.',
    'long_description': '# pencode\nBasic but fairly configurable Python FFMPEG CLI batch thing.\n',
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/pencode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
