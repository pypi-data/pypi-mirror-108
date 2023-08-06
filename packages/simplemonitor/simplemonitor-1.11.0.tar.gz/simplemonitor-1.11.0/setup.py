# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplemonitor',
 'simplemonitor.Alerters',
 'simplemonitor.Loggers',
 'simplemonitor.Monitors',
 'simplemonitor.util']

package_data = \
{'': ['*'], 'simplemonitor': ['html/*']}

install_requires = \
['Jinja2>=2.11.2,<4.0.0',
 'arrow>=0.17,<1.2',
 'boto3>=1.15.16,<2.0.0',
 'colorlog>=4.4,<6.0',
 'paho-mqtt>=1.5.1,<2.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'ping3>=2.6.6,<3.0.0',
 'psutil>=5.7.2,<6.0.0',
 'pyOpenSSL>=19.1,<21.0',
 'pyarlo>=0.2.4,<0.3.0',
 'requests>=2.24.0,<3.0.0',
 'ring-doorbell>=0.6.0',
 'twilio>=6.58.0,<7.0.0']

extras_require = \
{':sys_platform == "darwin"': ['pync>=2.0.3,<3.0.0'],
 ':sys_platform == "win32"': ['pywin32>=228,<302']}

entry_points = \
{'console_scripts': ['simplemonitor = simplemonitor.monitor:main',
                     'winmonitor = simplemonitor.winmonitor:main']}

setup_kwargs = {
    'name': 'simplemonitor',
    'version': '1.11.0',
    'description': 'A simple network and host monitor',
    'long_description': '[![PyPI version fury.io](https://badge.fury.io/py/simplemonitor.svg)](https://pypi.python.org/pypi/simplemonitor/) [![Downloads](https://pepy.tech/badge/simplemonitor)](https://pepy.tech/project/simplemonitor)\n\n![Tests (Windows)](https://github.com/jamesoff/simplemonitor/workflows/Tests%20(Windows)/badge.svg) ![Tests (Linux)](https://github.com/jamesoff/simplemonitor/workflows/Tests%20(Linux)/badge.svg) ![Linting](https://github.com/jamesoff/simplemonitor/workflows/Linting/badge.svg)\n\n[![codecov](https://codecov.io/gh/jamesoff/simplemonitor/branch/master/graph/badge.svg)](https://codecov.io/gh/jamesoff/simplemonitor) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSimpleMonitor is a Python script which monitors hosts and network connectivity. It is designed to be quick and easy to set up and lacks complex features that can make things like Nagios, OpenNMS and Zenoss overkill for a small business or home network. Remote monitor instances can send their results back to a central location.\n\nRequires Python >= 3.6.2.\n\nDocumentation is here:\nhttps://jamesoff.github.io/simplemonitor/\n',
    'author': 'James Seward',
    'author_email': 'james@jamesoff.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jamesoff/simplemonitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
