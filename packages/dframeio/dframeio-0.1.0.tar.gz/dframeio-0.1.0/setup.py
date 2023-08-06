# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dframeio', 'tests']

package_data = \
{'': ['*'],
 'tests': ['data/parquet/*',
           'data/parquet/multifile/*',
           'data/parquet/multifolder/gender=/*',
           'data/parquet/multifolder/gender=Female/*',
           'data/parquet/multifolder/gender=Male/*']}

install_requires = \
['pandas>=1.0.0,<2.0']

extras_require = \
{'pyarrow': ['pyarrow>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'dframeio',
    'version': '0.1.0',
    'description': ' Read and write dataframes anywhere.',
    'long_description': '# dataframe-io\n\n\n<a href="https://pypi.python.org/pypi/dframeio">\n    <img src="https://img.shields.io/pypi/v/dframeio.svg"\n        alt = "Release Status">\n</a>\n\n[![codecov](https://codecov.io/gh/chr1st1ank/dataframe-io/branch/master/graph/badge.svg?token=4oBkRHXbfa)](https://codecov.io/gh/chr1st1ank/dataframe-io)\n<a href="https://github.com/chr1st1ank/dframeio/actions">\n    <img src="https://github.com/chr1st1ank/dframeio/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://dframeio.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/dframeio/badge/?version=latest" alt="Documentation Status">\n</a>\n\n\n Read and write dataframes anywhere\n\n\n* Free software: Apache-2.0\n* Documentation: <https://dframeio.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Christian Krudewig',
    'author_email': 'chr1st1ank@krudewig-online.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chr1st1ank/dframeio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
