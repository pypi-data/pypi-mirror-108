# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_supervisor_plugin',
 'netbox_supervisor_plugin.api',
 'netbox_supervisor_plugin.migrations',
 'netbox_supervisor_plugin.tests']

package_data = \
{'': ['*'],
 'netbox_supervisor_plugin': ['templates/netbox_supervisor_plugin/*']}

setup_kwargs = {
    'name': 'netbox-supervisor-plugin',
    'version': '1.0.0',
    'description': 'plugin for netbox',
    'long_description': None,
    'author': 'Ilya Zakharov',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
