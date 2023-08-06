# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlikflow']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow-providers-telegram>=1.0.2,<2.0.0',
 'requests-ntlm>=1.1.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'zeep>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'qlikflow',
    'version': '1.0.14',
    'description': 'This module allows you to create simple Apache Airflow DAG files-constructors for QlikView, Qlik Sense and NPrinting.',
    'long_description': "![GitHub stars](https://img.shields.io/github/stars/bintocher/qlikflow.svg)\n![GitHub contributors](https://img.shields.io/github/contributors/bintocher/qlikflow.svg)\n![GitHub license](https://img.shields.io/github/license/bintocher/qlikflow.svg)\n![Pipy Installs](https://img.shields.io/pypi/dm/qlikflow)\n![Last commit](https://img.shields.io/github/last-commit/bintocher/qlikflow)\n![Issues](https://img.shields.io/github/issues/bintocher/qlikflow)\n\n# qlikflow\n\nThis module allows you to create simple Apache Airflow DAG files-constructors for QlikView, Qlik Sense and NPrinting.\n\n## Information files\n\n- Changelog : https://github.com/bintocher/qlikflow/blob/main/CHANGELOG.md\n\n- Manual(en) : https://github.com/bintocher/qlikflow/blob/main/doc/readme.md\n\n- This readme : https://github.com/bintocher/qlikflow/blob/main/README.md\n\n## Install\n\n``` bash\npip3 install qlikflow\n```\n\n## Upgrade\n\n``` bash\npip3 install qlikflow -U\n```\n\n## Create config-file\n\nOpen ``config_generator.py`` with your IDE editor, and set settings, save script\n\nThen run script to create ``config.json`` file\n\nPut this ``config.json`` file on your Apache Airflow server in folder: ``AIRFLOW_HOME/config/``\n\n## Use in DAG-files\n\n``` python\n\nfrom airflow import DAG\nfrom airflow.utils.dates import days_ago\nfrom qlikflow import qlikflow\nfrom datetime import datetime\n\n\ntasksDict = {\n    u'qliksense. Test task': {\n        'Soft' : 'qs1',\n        'TaskId' : 'c5d80e71-f574-4655-8874-3a6e2aed6218',\n        'RandomStartDelay' : 10, \n        },\n    u'np100. run nprinting tasks' : {\n        'Soft' : 'np100',\n        'TaskId' : [\n            'taskid1',\n            'taskid2',\n            'taskid3',\n            'taskid4',\n        ],\n        'Dep' : {\n            u'qliksense. Test task',\n            }\n        }\n    }\n\ndefault_args  = {\n    'owner': 'test',\n    'depends_on_past': False,\n}\n\ndag = DAG(\n    dag_id = '_my_test_dag',\n    default_args = default_args ,\n    start_date = days_ago(1),\n    schedule_interval = '@daily',\n    description = 'Default test dag',\n    tags = ['qliksense', 'testing'],\n    catchup = False\n)\n\nairflowTasksDict = {}\nqlikflow.create_tasks(tasksDict, airflowTasksDict, dag)\n```\n\nThis code convert into DAG like this:\n\n![image](https://user-images.githubusercontent.com/8188055/117771014-020b1600-b279-11eb-9565-de198a12c9e2.png)\n",
    'author': 'bintocher',
    'author_email': 'schernov1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bintocher/qlikflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
