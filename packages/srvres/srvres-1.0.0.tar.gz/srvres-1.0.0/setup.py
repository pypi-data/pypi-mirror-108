# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srvres']

package_data = \
{'': ['*']}

install_requires = \
['dnspython']

setup_kwargs = {
    'name': 'srvres',
    'version': '1.0.0',
    'description': 'A somewhat simple-- yet useful-- SRV resolver in around 100 lines of Python code.',
    'long_description': '# srvres\n\nA somewhat simple-- yet useful-- SRV resolver in around 100 lines of Python code.\n\n## How to use\n\n```python\nimport srvres, socket\n\nsock = None\nfor target in srvres.SRVResolver("xmpp-client","xmpp.example.com"):\n\tsock = socket.socket()\n\tsock.settimeout(5)\n\ttry:\n\t\tsock.connect(target)\n\t\tbreak\n\texcept socket.timeout: pass\nif sock is None:\n\t# the service is unavailable\nelse:\n\t# the service is available and connected to\n```\n\n## Explanation\n\nThe magic occurs in the `srvres.SRVResolver` object. When you iterate over a SRVResolver object, it makes the DNS query for the SRV record for the specified service. If it gets an answer, it returns a `srvres.SRVResolver.Iterator` object, which handles priority and weighting. If it doesn\'t get an answer, it falls back to the given domain and a known port (if a port is known). If a port is not known, the default response will include a port of 0. This can be changed by supplying a `port` argument to the `srvres.SRVResolver` constructor like so:\n\n```\n# "unknownprotocol" listens on port 49151\nfor target in srvres.SRVResolver("unknownprotocol","example.com",port=49151):\n\t# now the unknown response will have port 49151 as opposed to 0\n```\n\n## What ports are classified as "known"?\n\nWhen you first import the library, it will download the IANA registry of assigned service names and port numbers, which it ports into a format it can more easily use. It also downloads a separate registry, maintained by me, that includes a handful of other useful ports that aren\'t defined by the IANA registry.\n\nBasically, if you have an IANA registration for your service name, and it includes a port and transport, you\'ll be able to use your service name with no issues. If you don\'t, and your service is a widely used one, ask me and I\'ll probably add it to my list.\n',
    'author': 'Robert "khuxkm" Miles',
    'author_email': 'khuxkm+srvres@tilde.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MineRobber9000/srvres',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
