# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['songmam',
 'songmam.models',
 'songmam.models.messaging',
 'songmam.models.messaging.templates',
 'songmam.models.messaging.templates.airline',
 'songmam.models.messenger_profile',
 'songmam.models.webhook',
 'songmam.models.webhook.events',
 'songmam.models.webhook.events.message']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17,<1.2',
 'autoname>=1.0.0,<2.0.0',
 'avajana>=0.4,<0.5',
 'fastapi>=0.61.2,<0.62.0',
 'furl>=2.1.0,<3.0.0',
 'httpx>=0.16.1,<0.17.0',
 'loguru>=0.5.1,<0.6.0',
 'moshimoshi>=0.2,<0.3',
 'parse>=1.16.0,<2.0.0',
 'path>=15.0.0,<16.0.0']

entry_points = \
{'console_scripts': ['songmam = songmam.__main__:app']}

setup_kwargs = {
    'name': 'songmam',
    'version': '1.10.0',
    'description': 'a facebook messenger hypermodern python library based on fastapi. ',
    'long_description': '<p align="center">\n  <a href="https://codustry.com/technologies/songmam">\n    <img alt="babel" src="https://storage.googleapis.com/codustry_assets/github/icon-shadow-songmam.png" height="100">\n  </a>\n</p>\n\n\n# Songmam\n\na facebook messenger hypermodern python library based on fastapi. \n\n\n<div align="center">\n\n[![Build status](https://github.com/codustry/songmam/workflows/build/badge.svg?branch=master&event=push)](https://github.com/codustry/songmam/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/songmam.svg)](https://pypi.org/project/songmam/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/codustry/songmam/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/codustry/songmam/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/codustry/songmam/releases)\n[![License](https://img.shields.io/github/license/codustry/songmam)](https://github.com/codustry/songmam/blob/master/LICENSE)\n\n</div>\n\n\n\n## Features\n\n- Async\n- based on Pydantic, easy to work with `FastApi`\n- 1-1 structure to official facebook documentation\n\n  \n## Installation \n\n```bash\npip install songmam\n```\n## Documentation\n\n[Documentation](https://linktodocumentation)\n\n  \n## Usage/Examples\n\nThere are a few examples under the folder, `examples`\n\n```python\nimport Component from \'my-project\'\n\nfunction App() {\n  return <Component />\n}\n```\n\n  \n## Used By\n\nThis project is used by the following companies:\n\n- Codustry\n  - Gebwai\n  - Saku Chatbot\n\n  \n## Authors\n\n- [@circleoncircles](https://www.github.com/kcircleoncircles)\n\n  \n## Feedback\n\nIf you have any feedback, please reach out to us at saku@coudstry.com\n\n  \n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/codustry/songmam)](https://github.com/codustry/songmam/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/codustry/songmam/blob/master/LICENSE) for more details.\n\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'codustry',
    'author_email': 'hello@codustry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codustry/songmam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
