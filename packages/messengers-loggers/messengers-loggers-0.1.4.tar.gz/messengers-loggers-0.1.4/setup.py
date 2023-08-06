# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['messengers_loggers',
 'messengers_loggers.slack',
 'messengers_loggers.telegram',
 'messengers_loggers.utils',
 'messengers_loggers.vk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

extras_require = \
{'test': ['pytest>=5.4.3,<6.0.0']}

setup_kwargs = {
    'name': 'messengers-loggers',
    'version': '0.1.4',
    'description': 'Loggers for sending log to messengers',
    'long_description': None,
    'author': 'arck1',
    'author_email': 'a.v.rakhimov@gmail.com',
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
