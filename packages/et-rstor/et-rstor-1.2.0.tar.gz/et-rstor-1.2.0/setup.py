# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_rstor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'et-rstor',
    'version': '1.2.0',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '========\net-rstor\n========\n\n\n\n<Enter a one-sentence description of this project here.>\n\n\n* Free software: GNU General Public License v3\n* Documentation: https://et-rstor.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Bert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-rstor',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
