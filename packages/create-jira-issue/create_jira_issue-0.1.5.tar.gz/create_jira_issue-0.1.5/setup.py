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
    'version': '0.1.5',
    'description': 'CLI app to create issues in Jira from console',
    'long_description': '# create_jira_issue\n\n##Description\nThis command line app will help you to create issues from console\n##Usage\n```shell\ncjiss -s "Your issue summary" -d "your issue description" -n "./settings.yml" --sprint\n```\n##Arguments\n_s_ - [MANDATORY] issue summary\n\n_d_ - issue description\n\n_n_ - path to your issue settings in yaml (see below). If not provided, file with name "settings.yml" will be looked in\nthe current directory\n\n_sprint_ - issue will be added to current sprint.\n\n##Settings\n```yaml\n# fill this to make the script work\n\n# your jira url\njira_url: https://your.jira.url.com\n# login in jira\nlogin: your_login\n# pass in jira\npassword: your_pass\n# project you work in\nproject: PROJECT\n# jira issue type (epic, issue, etc) id\n# 3 stands for issue\nissue_type: 3\n# default priority id\npriority_id: 4\n# default assignee\nassignee: assignee_login\n# default assignee\nreporter: your_login\n# your jira board id\nboard_id: 20801\n# labels to add\nlabels:\n  - new\n```',
    'author': 'Dmitrii Akhmetshin',
    'author_email': 'elevation1987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/44dw/create_jira_issue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
