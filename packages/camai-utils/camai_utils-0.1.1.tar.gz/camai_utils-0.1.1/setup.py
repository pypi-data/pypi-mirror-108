# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camai_utils',
 'camai_utils.processing',
 'camai_utils.processing.csvs',
 'camai_utils.processing.images',
 'camai_utils.processing.pdfs',
 'camai_utils.processing.pdfs..ipynb_checkpoints',
 'camai_utils.processing.text']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'fastapi[all]>=0.65.1,<0.66.0',
 'hl7>=0.4.2,<0.5.0',
 'pandas>=1.2.4,<2.0.0',
 'pdf2image>=1.15.1,<2.0.0',
 'phonenumbers>=8.12.23,<9.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'pytest>=6.2.4,<7.0.0',
 'regex>=2021.4.4,<2022.0.0']

setup_kwargs = {
    'name': 'camai-utils',
    'version': '0.1.1',
    'description': 'Python utils for the Camai CHC COVID Datasystem.',
    'long_description': None,
    'author': 'apteryxlabs',
    'author_email': 'matthew@apteryxlabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
