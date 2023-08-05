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
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
