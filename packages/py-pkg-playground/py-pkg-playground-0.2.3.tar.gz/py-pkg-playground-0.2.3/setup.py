# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_pkg_playground']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-pkg-playground',
    'version': '0.2.3',
    'description': 'This is a Python package to learn Github actions!',
    'long_description': '# py-pkg-playground\n\n[![Build Status](https://github.com/Dresdn/py-pkg-playground/workflows/test/badge.svg?branch=main&event=push)](https://github.com/Dresdn/py-pkg-playground/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/Dresdn/py-pkg-playground/branch/main/graph/badge.svg)](https://codecov.io/gh/Dresdn/py-pkg-playground)\n[![Python Version](https://img.shields.io/pypi/pyversions/py-pkg-playground.svg)](https://pypi.org/project/py-pkg-playground/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nThis is a Python package to learn Github actions!\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n## Installation\n\n```bash\npip install py-pkg-playground\n```\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom py_pkg_playground.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[MIT](https://github.com/Dresdn/py-pkg-playground/blob/master/LICENSE)\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [bb1dd122f276580008375990122e1e3f71394275](https://github.com/wemake-services/wemake-python-package/tree/bb1dd122f276580008375990122e1e3f71394275). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/bb1dd122f276580008375990122e1e3f71394275...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dresdn/py-pkg-playground',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
