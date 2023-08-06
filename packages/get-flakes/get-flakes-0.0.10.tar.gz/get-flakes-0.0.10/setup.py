# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['get-flakes', 'get-flakes.backend']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.17,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'coverage>=5.5,<6.0',
 'fastapi[all]>=0.65.1,<0.66.0',
 'gunicorn>=20.1.0,<21.0.0',
 'junitparser>=2.0.0,<3.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.13.0,<10.0.0',
 'sqlalchemy-cockroachdb>=1.3.3,<2.0.0',
 'timeago>=1.0.15,<2.0.0']

entry_points = \
{'console_scripts': ['get-flakes = get-flakes.cli:run'],
 'pytest11': ['get-flakes = get-flakes.pytest_plugin']}

setup_kwargs = {
    'name': 'get-flakes',
    'version': '0.0.10',
    'description': 'get-flakes',
    'long_description': None,
    'author': 'alex-treebeard',
    'author_email': 'alex@treebeard.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/treebeardtech/get-flakes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
