# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pybrainyquote']
install_requires = \
['bs4', 'furl', 'requests']

setup_kwargs = {
    'name': 'pybrainyquote',
    'version': '0.6',
    'description': 'Get quotes from brainyquote. Make you life positive.',
    'long_description': '==============\nPyBrainyquote\n==============\n\nGet quotes from brainyquote. Make you life positive.\n\nRequirements\n-------------\n\nrequests\n\nbs4\n\nfurl\n\n\nDownload\n---------\n\npip install pybrainyquote\n\n\nWhy\n--------\n\nThe original one `brainyquote` is too simple. \n\n\n\nGrammar\n--------\n    \nimport::\n\n    from pybrainyquote import *\n\n\nget quotes::\n\n    Quote.today(topic=what you like) # get today topic\n    get_popular_topics() # have a look at the lists popular topics, if you do not have any idea\n    get_topics()\n    get_authors()\n\n    # just try the following\n    Quote.find_all(topic)\n    Quote.find(topic)\n    Quote.find(topic)\n\n    Quote.choice_yaml(yamlfile) # choose a quote in yaml files randomly\n    Quote.read_yaml(yamlfile)\n\nFuture\n-------\nDefine a search engine for quotes, and a method to get one quote randomly. (Completed partly)',
    'author': 'William Song',
    'author_email': '30965609+Freakwill@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Freakwill/pybrainyquote',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
