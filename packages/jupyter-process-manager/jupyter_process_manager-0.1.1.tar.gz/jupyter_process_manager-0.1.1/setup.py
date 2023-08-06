# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter_process_manager']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.61.0,<5.0.0',
 'yaspin']

setup_kwargs = {
    'name': 'jupyter-process-manager',
    'version': '0.1.1',
    'description': 'python package with widget to simplify work with many processes in jupyter',
    'long_description': None,
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
