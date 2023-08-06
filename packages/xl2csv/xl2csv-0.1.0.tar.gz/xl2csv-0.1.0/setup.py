# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xl2csv']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.7,<4.0.0', 'python-slugify>=5.0.2,<6.0.0']

entry_points = \
{'console_scripts': ['xl2csv = xl2csv.convert:main']}

setup_kwargs = {
    'name': 'xl2csv',
    'version': '0.1.0',
    'description': 'A tool to convert an Excel file consisting of multiple worksheets to individual CSV files.',
    'long_description': '# Excel to CSV Converter\n\nA tool to convert an Excel file consisting of multiple worksheets to individual CSV files.\n',
    'author': 'Jarno Timmermans',
    'author_email': 'netletic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/netletic/xl2csv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
