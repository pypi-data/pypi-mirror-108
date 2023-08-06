# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qiyu_token',
 'django_qiyu_token.admin',
 'django_qiyu_token.migrations',
 'django_qiyu_token.models']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<3.3']

setup_kwargs = {
    'name': 'django-qiyu-token',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
