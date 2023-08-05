# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nepse', 'nepse.security']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.2,<5.0.0', 'httpx>=0.18.1,<0.19.0', 'pyhumps>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'nepse-api',
    'version': '0.5.0',
    'description': 'This is a API wrapper for NEPSE API.',
    'long_description': '# NEPSE API Wrapper\n\nThis python module fetches the data from [Nepali Stock Site](https://newweb.nepalstock.com/) and provides them in a pythonic\nand usable way.\n\n\n## About\n\nThis is a API wrapper for NEPSE API. This project was inspired from [PyPi Nepse](https://github.com/pyFrappe/nepse). \n\n## How to use?\n\nYou can use this by package from [Nepse API PyPi](https://pypi.org/project/nepse-api/)\n```sh\npip install nepse-api\n```\n\n## Why use this?\n\nHow is this better than [PyPi Nepse](https://github.com/pyFrappe/nepse)?\n- It is asynchronous.\n- Data can be taken as attributes rather than from dict.\n- Data is fetched from the API rather than scraping the site.\n- Data is cached \n\n## APIs used\n\nThe APIs that I used to create this API wrapper is:\n- https://newweb.nepalstock.com/api/\n\n## How to use?\n\n```py\nimport asyncio\nfrom nepse import Client\n\nasync def main():\n    # Initializes the client\n    client = Client()\n\n    # Gets the data\n    data = await client.security_client.get_company(symbol="UPPER")\n\n    # Prints the highest price for that company today\n    print(data.security_daily_trade_dto.high_price)\n\n    # Properly closes the session\n    await client.close()\n    \n# Run the function\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n## Why are the attributes so in-costistent?\n\nThe attribues are in-consistent because the attributes are set according to the response set by the API. I tried changing \nit up but that would be distruptive because the comability with the API would be broken. \n\n## Documentation?\n\nDocumentation is still in progress!\n\n## Want To Contribute?\n\nYou can send a pull request or open an issue to contribute.',
    'author': 'Samrid Pandit',
    'author_email': 'samrid.pandit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samrid-Pandit/nepse-api/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
