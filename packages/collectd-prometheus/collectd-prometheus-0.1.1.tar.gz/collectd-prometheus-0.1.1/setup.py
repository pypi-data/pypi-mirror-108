# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['collectd_prometheus']
install_requires = \
['prometheus-client>=0.7.1,<0.8.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'collectd-prometheus',
    'version': '0.1.1',
    'description': 'collectd plugin to read Prometheus metrics endpoints',
    'long_description': None,
    'author': 'Ryar Nyah',
    'author_email': 'ryarnyah@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
