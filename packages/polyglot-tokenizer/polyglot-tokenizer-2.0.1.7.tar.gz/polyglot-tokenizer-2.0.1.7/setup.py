# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyglot_tokenizer', 'polyglot_tokenizer.tests']

package_data = \
{'': ['*'], 'polyglot_tokenizer': ['data/*']}

setup_kwargs = {
    'name': 'polyglot-tokenizer',
    'version': '2.0.1.7',
    'description': "Tokenizer for world's most spoken languages and social media texts like Facebook, Twitter etc.",
    'long_description': None,
    'author': 'irshadbhat',
    'author_email': 'bhatirshad127@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
