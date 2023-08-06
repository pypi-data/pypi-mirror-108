# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ohnodb']

package_data = \
{'': ['*']}

install_requires = \
['schema>=0.7.4,<0.8.0']

setup_kwargs = {
    'name': 'ohnodb',
    'version': '1.0.1',
    'description': 'A very, very bad database',
    'long_description': '# ohnodb\n\n## Please never use this in production. I beg you, don\'t.\n\n``` pip install ohnodb ```\n\nUsage:\n\n```py\nfrom ohnodb import OhNoDB\n\ndb = OhNoDB("./data")\n\nmy_data = {\n    "hello":"world"\n}\n\ndb.create("my_table", "my_item", my_data, is_json=True)\n\nprint(db.fetch("my_table", "my_item", is_json=True))  # >>> {"hello": "world"}\n\ndb.update("my_table", "my_item", {}, is_json=True)\n\nprint(db.fetch("my_table", "my_item", is_json=True))  # >>> {}\n```\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/ohnodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
