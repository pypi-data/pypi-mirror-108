# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['step_exec_lib', 'step_exec_lib.utils']

package_data = \
{'': ['*']}

install_requires = \
['configargparse>=1.4.1,<2.0.0',
 'gitpython>=3.1.17,<4.0.0',
 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'step-exec-lib',
    'version': '0.1.0',
    'description': 'A library that helps execute pipeline of tasks using filters and simple composition',
    'long_description': '[![build](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml/badge.svg)](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/giantswarm/step-exec-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/giantswarm/step-exec-lib)\n[![PyPI Version](https://img.shields.io/pypi/v/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)\n[![Apache License](https://img.shields.io/badge/license-apache-blue.svg)](https://pypi.org/project/step-exec-lib/)\n\n# step-exec-lib\n\nA simple library to easily orchestrate a set of Steps into a filtrable pipeline.\n\n**Disclaimer**: docs are still work-in-progress!\n\nEach step provides a defined set of actions. When a pipeline is execute first all `pre` actions\nof all Steps are executed, then `run` actions and so on. Steps can provide labels, so\nyou can easily disable/enable a subset of steps.\n\nA ready to use python app template. Based on `pipenv`.\n',
    'author': 'Łukasz Piątkowski',
    'author_email': 'lukasz@giantswarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantswarm/step-exec-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
