# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyyaledoorman']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'traitlets>=5.0.5,<6.0.0']

setup_kwargs = {
    'name': 'pyyaledoorman',
    'version': '1.0.7',
    'description': 'Python library for the Yale Doorman Smart API',
    'long_description': 'Pyyaledoorman\n=============\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/pyyaledoorman.svg\n   :target: https://pypi.org/project/pyyaledoorman/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pyyaledoorman\n   :target: https://pypi.org/project/pyyaledoorman\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/pyyaledoorman\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pyyaledoorman/latest.svg?label=Read%20the%20Docs\n   :target: https://pyyaledoorman.readthedocs.io/\n   :alt: Read the documentation at https://pyyaledoorman.readthedocs.io/\n.. |Tests| image:: https://github.com/espenfjo/pyyaledoorman/workflows/Tests/badge.svg\n   :target: https://github.com/espenfjo/pyyaledoorman/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/espenfjo/pyyaledoorman/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/espenfjo/pyyaledoorman\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nA Python library for interfacing with the Yale Doorman Home API.\n\nFeatures\n--------\n\n* Read whether lock is unlocked, locked, or door open\n* Locking / Unlocking\n* Enabling / Disabling auto lock\n* Reading Volume level, Language, Auto lock disabled/enabled\n\n\n\nRequirements\n------------\n\n* Yale Doorman home user account.\n\n\nInstallation\n------------\n\nYou can install *Pyyaledoorman* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install pyyaledoorman\n\n\nUsage\n-----\n\nPlease see `Usage <Usage_>`_ for details.\n\n.. code-example\n.. code-block:: python\n\n    import pyyaledoorman\n    import aiohttp\n    import asyncio\n    import pyyaledoorman\n\n\n    async def main():\n        async with aiohttp.ClientSession() as session:\n            client = pyyaledoorman.Client(\n                "username",\n                "password",\n                session=session,\n            )\n            assert await client.login() == True\n            await client.update_devices()\n\n            for device in client.devices:\n                print(device.name)\n                await device.disable_autolock()\n                await device.unlock(pincode="123456")\n\n\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n\n.. code-example-end\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Pyyaledoorman* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/espenfjo/pyyaledoorman/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://pyyaledoorman.readthedocs.io/en/latest/usage.html\n',
    'author': 'Espen Fjellvær Olsen',
    'author_email': 'espen@mrfjo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/espenfjo/pyyaledoorman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
