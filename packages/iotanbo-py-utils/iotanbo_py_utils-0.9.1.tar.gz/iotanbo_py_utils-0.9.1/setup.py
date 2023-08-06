# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iotanbo_py_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pathvalidate>=2.4.1,<3.0.0', 'result>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['iotanbo_py_utils = iotanbo_py_utils.__main__:main']}

setup_kwargs = {
    'name': 'iotanbo-py-utils',
    'version': '0.9.1',
    'description': 'Python utilities by iotanbo',
    'long_description': 'Iotanbo Python Utilities\n========================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/iotanbo_py_utils.svg\n   :target: https://pypi.org/project/iotanbo_py_utils/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/iotanbo_py_utils\n   :target: https://pypi.org/project/iotanbo_py_utils\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/iotanbo_py_utils\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/iotanbo_py_utils/latest.svg?label=Read%20the%20Docs\n   :target: https://iotanbo_py_utils.readthedocs.io/\n   :alt: Read the documentation at https://iotanbo_py_utils.readthedocs.io/\n.. |Tests| image:: https://github.com/iotanbo/iotanbo_py_utils/workflows/Tests/badge.svg\n   :target: https://github.com/iotanbo/iotanbo_py_utils/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/iotanbo/iotanbo_py_utils/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/iotanbo/iotanbo_py_utils\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nInstallation\n------------\n\nYou can install *Iotanbo Python Utilities* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install iotanbo_py_utils\n\n\nUsage\n-----\n\nThis package was initially intended for internal usage.\nSee the API reference for more information.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Iotanbo Python Utilities* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _file an issue: https://github.com/iotanbo/iotanbo_py_utils/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://iotanbo_py_utils.readthedocs.io/en/latest/usage.html\n',
    'author': 'iotanbo',
    'author_email': 'yurizappo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iotanbo/iotanbo_py_utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
