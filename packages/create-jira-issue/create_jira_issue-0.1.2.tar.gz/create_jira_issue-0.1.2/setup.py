# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['create_jira_issue']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'argparse>=1.4.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'url-normalize>=1.4.3,<2.0.0',
 'urllib3>=1.26.5,<2.0.0']

entry_points = \
{'console_scripts': ['cjiss = create_jira_issue.create_jira_issue:main']}

setup_kwargs = {
    'name': 'create-jira-issue',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Dmitrii Akhmetshin',
    'author_email': 'elevation1987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
