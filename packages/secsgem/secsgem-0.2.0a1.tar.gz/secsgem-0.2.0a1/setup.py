# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secsgem',
 'secsgem.common',
 'secsgem.gem',
 'secsgem.hsms',
 'secsgem.secs',
 'secsgem.secs.data_items',
 'secsgem.secs.functions',
 'secsgem.secs.variables']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'transitions>=0.8.8,<0.9.0']

setup_kwargs = {
    'name': 'secsgem',
    'version': '0.2.0a1',
    'description': 'Python SECS/GEM implementation',
    'long_description': '# secsgem\nSimple Python SECS/GEM implementation\n\nThis module is still work in progress. I\'d love to get your input, your use case, whether you are experienced in SECS or not.\n\n[![Test Coverage](https://api.codeclimate.com/v1/badges/223821436f063223b9da/test_coverage)](https://codeclimate.com/github/bparzella/secsgem/test_coverage)\n[![Maintainability](https://api.codeclimate.com/v1/badges/223821436f063223b9da/maintainability)](https://codeclimate.com/github/bparzella/secsgem/maintainability)\n[![Tests](https://github.com/bparzella/secsgem/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/bparzella/secsgem/actions/workflows/run_tests.yaml)\n[![Image](https://readthedocs.org/projects/secsgem/badge/)](http://secsgem.readthedocs.org/en/latest/)\n\n\n## Installation\nTo install the latest official release (0.1.0, 2020-05-27, https://pypi.python.org/pypi/secsgem):\n\n```bash\n$ pip install secsgem\n```\n\nTo install the current development code (might be instable):\n\n```bash\n$ pip install git+git://github.com/bparzella/secsgem\n```\n\n## Sample\n\n```python\nimport logging\nimport code\n\nimport secsgem.gem\n\nfrom communication_log_file_handler import CommunicationLogFileHandler\n\nclass SampleHost(secsgem.gem.GemHostHandler):\n    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):\n        secsgem.gem.GemHostHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)\n\n        self.MDLN = "gemhost"\n        self.SOFTREV = "1.0.0"\n\ncommLogFileHandler = CommunicationLogFileHandler("log", "h")\ncommLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))\nlogging.getLogger("hsms_communication").addHandler(commLogFileHandler)\nlogging.getLogger("hsms_communication").propagate = False\n\nlogging.basicConfig(format=\'%(asctime)s %(name)s.%(funcName)s: %(message)s\', level=logging.DEBUG)\n\nh = SampleHost("127.0.0.1", 5000, True, 0, "samplehost")\nh.enable()\n\ncode.interact("host object is available as variable \'h\'", local=locals())\n\nh.disable()\n```\n\n## Contribute\n\nThis project is still at its beginning. If you can offer suggestions, additional information or help please contact me.\n',
    'author': 'Benjamin Parzella',
    'author_email': 'bparzella@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bparzella/secsgem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
