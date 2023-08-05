# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_packager']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['lambda-packager = lambda_packager:run_cli']}

setup_kwargs = {
    'name': 'lambda-packager',
    'version': '0.6.1',
    'description': 'Stop writing your own scripts and let this package your python aws lambda zips for you',
    'long_description': '# lambda-packager\n\nCurrently, requires python >=3.8 and later due to [required features of copytree](https://docs.python.org/3/library/shutil.html#shutil.copytree)\n\n##Usage\n- Just run the packager with:\n```bash\n$ lambda-packager\n # or if not in the project directory  \n$ lambda-packager path/to/project/dir\n```\n- lambda-packager will include any dependencies defined in\n    - poetry (pyproject.toml)\n    - requirements.txt\n    - ~~Pipenv~~ (Coming soon!)\n- By default lambda-packager will include all src files that match `*.py`\n- You can customise this with the following config:\n```toml\n[tool.lambda-packager]\nsrc_patterns = ["lambda_packager/*.py"]\n```\n\n### Hidden files\n- hidden files and folders are ignored by default when including src files\n- if you wish to disable this then add the following config to you pyproject.toml\n```toml\n[tool.lambda-packager]\nignore_hidden_files = false\n```\n\n### Ignore folders\nIf there are folders that you wish always exclude then you can use `ignore_folders`\nNote: `ignore_folders` is always respected even if there was a match via `src_patterns`\n```toml\n[tool.lambda-packager]\nignore_folders = ["venv"]\n```\n\n## License\n\nThis code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").\n',
    'author': 'cob16',
    'author_email': 'public+github@cormacbrady.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmrc/python-aws-lambda-packager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
