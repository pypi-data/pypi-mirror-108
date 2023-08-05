# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royston']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.0.0,<2.0.0',
 'gensim>=4.0.1,<5.0.0',
 'nltk>=3.6.2,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'royston',
    'version': '0.0.8',
    'description': 'A real time trend detection algorithm\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D',
    'long_description': None,
    'author': 'Ian Read',
    'author_email': 'ianharveyread@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
