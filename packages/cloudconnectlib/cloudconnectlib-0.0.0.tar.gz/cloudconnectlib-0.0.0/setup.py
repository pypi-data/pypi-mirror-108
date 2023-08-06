# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudconnectlib',
 'cloudconnectlib.common',
 'cloudconnectlib.configuration',
 'cloudconnectlib.core',
 'cloudconnectlib.core.cacerts',
 'cloudconnectlib.splunktacollectorlib',
 'cloudconnectlib.splunktacollectorlib.common',
 'cloudconnectlib.splunktacollectorlib.data_collection']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.0.2,<6.0.0',
 'future',
 'httplib2==0.19.1',
 'jinja2==2.10.1',
 'jsl>=0.2.4,<0.3.0',
 'jsonpath-rw==1.4.0',
 'jsonschema>=3.2.0,<4.0.0',
 'munch==2.3.2',
 'requests>=2.25.1,<3.0.0',
 'six',
 'solnlib==3.0.5',
 'sortedcontainers==2.3.0',
 'splunk-sdk==1.6.15',
 'splunktalib>=1.2.1,<2.0.0',
 'splunktaucclib==4.1.2']

setup_kwargs = {
    'name': 'cloudconnectlib',
    'version': '0.0.0',
    'description': 'APP Cloud Connect',
    'long_description': None,
    'author': 'Addon Factory template',
    'author_email': 'addonfactory@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
