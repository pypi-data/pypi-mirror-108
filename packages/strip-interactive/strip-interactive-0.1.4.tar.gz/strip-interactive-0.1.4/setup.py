# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strip_interactive']

package_data = \
{'': ['*'], 'strip_interactive': ['.git/*', '.git/hooks/*', '.git/info/*']}

setup_kwargs = {
    'name': 'strip-interactive',
    'version': '0.1.4',
    'description': 'Strip and execute interactive Python string',
    'long_description': '# Strip Interactive Python String\n\nHave you ever come across an online tutorial that shows interactive Python code like this:\n\n```python\n>>> import numpy as np\n>>> print(np.array([1,2,3]))\narray([1, 2, 3])\n```\n\nand wished to run only the inputs like below?\n\n```python\nimport numpy as np\nprint(np.array([1,2,3]))\n```\n\nThat is when strip-interactive comes in handy. \n\n## Usage\nTo use strip-interactive, simply add the code you want to run to `run_interactive` method.\n\n```python\nfrom strip_interactive import run_interactive\n\ncode = """\n>>> import numpy as np\n>>> print(np.array([1,2,3]))\narray([1, 2, 3])\n"""\n\noutputs = run_interactive(code)\n```\n\nOutput:\n```bash\n[1 2 3]\n```\nYou can also get the clean code (without inputs and `>>>`) using `get_clean_code` method.\n\n```python\nfrom strip_interactive import get_clean_code\n\ncode = """\n>>> import numpy as np\n>>> print(np.array([1,2,3]))\narray([1, 2, 3])\n"""\n\ninputs = get_clean_code(code)\nprint(inputs)\n```\nOutput:\n```bash\nimport numpy as np\nprint(np.array([1,2,3]))\n```\n## Installation\n```bash\npip install strip-interactive\n```\n',
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/strip_interactive',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
