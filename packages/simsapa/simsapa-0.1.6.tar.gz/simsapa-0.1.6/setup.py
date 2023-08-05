# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simsapa',
 'simsapa.app',
 'simsapa.assets',
 'simsapa.assets.ui',
 'simsapa.layouts']

package_data = \
{'': ['*'],
 'simsapa.assets': ['icons/*', 'icons/32x32/*', 'icons/gif/*', 'icons/svg/*']}

install_requires = \
['Markdown>=3.3.4,<4.0.0',
 'PyPDF2>=1.26.0,<2.0.0',
 'PyQt5==5.15.0',
 'PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy-Utils>=0.37.2,<0.38.0',
 'SQLAlchemy>=1.4.6,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'epub_meta>=0.0.7,<0.0.8',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'semver>=2.13.0,<3.0.0']

extras_require = \
{':sys_platform == "darwin"': ['PyMuPDF>=1.18.13,<2.0.0'],
 ':sys_platform == "linux" and platform_machine == "x86_64"': ['PyMuPDF>=1.18.13,<2.0.0'],
 ':sys_platform == "win32"': ['PyMuPDF>=1.18.13,<2.0.0']}

setup_kwargs = {
    'name': 'simsapa',
    'version': '0.1.6',
    'description': 'Simsapa Dhamma Reader',
    'long_description': None,
    'author': 'Gambhiro',
    'author_email': 'gambhiro.bhikkhu.85@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
