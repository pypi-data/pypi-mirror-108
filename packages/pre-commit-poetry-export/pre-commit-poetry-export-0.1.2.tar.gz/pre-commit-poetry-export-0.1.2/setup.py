# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_poetry_export']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry-export = '
                     'pre_commit_poetry_export.poetry_export:main']}

setup_kwargs = {
    'name': 'pre-commit-poetry-export',
    'version': '0.1.2',
    'description': 'pre-commit hook to keep requirements.txt updated',
    'long_description': "# pre-commit-poetry-export\npre-commit hook to keep requirements.txt updated\n\n### Why?\nYour life is easier and the build is faster if you use requirements.txt file to install dependencies inside a docker image. But, it's not hard to forget to update the requirements file using poetry export and remember only when CI can't build the image.\n\n### How it Works\nIn every commit this hook runs the following steps:\n- If requirements.txt doesn't exist\n    - It will be created and hook fails\n\n- If requirements.txt exists\n    - The hook will copy it's content to a file named old.requirements.txt\n    - Then it will generate another requirements.txt using `poetry export` and compare the content of the two files\n    - If they match you're good to go, if not the hook fails with 'requirements updated' message\n\nIf the hook has updated or created your requirements file, you can now `git add requirements.txt` and finish your commit.\n\nFound any issues or want to suggest an improvement in the code?\nPlease contribute, open an issue /[here](https://github.com/avlm/pre-commit-poetry-export/issues/new)\n\nThanks! :)\n",
    'author': 'Antonio Luckwu',
    'author_email': 'victor.luckwu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avlm/pre-commit-poetry-export',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
