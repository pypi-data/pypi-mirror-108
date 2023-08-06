# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pricehist', 'pricehist.outputs', 'pricehist.resources', 'pricehist.sources']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.1.0,<2.0.0',
 'curlify>=2.2.1,<3.0.0',
 'lxml>=4.6.2,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pricehist = pricehist.cli:cli']}

setup_kwargs = {
    'name': 'pricehist',
    'version': '0.1.0',
    'description': 'Fetch and format historical price data',
    'long_description': "# pricehist\n\nA command-line tool for fetching and formatting historical price data, with\nsupport for multiple data sources and output formats.\n\n## Installation\n\nInstall via [pip](https://packaging.python.org/tutorials/installing-packages/#use-pip-for-installing):\n\n```bash\npip install pricehist\n```\n\n## Sources\n\n- **`alphavantage`**: [Alpha Vantage](https://www.alphavantage.co/)\n- **`coindesk`**: [CoinDesk Bitcoin Price Index](https://www.coindesk.com/coindesk-api)\n- **`coinmarketcap`**: [CoinMarketCap](https://coinmarketcap.com/)\n- **`ecb`**: [European Central Bank Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/index.en.html)\n- **`yahoo`**: [Yahoo! Finance](https://finance.yahoo.com/)\n\n## Output formats\n\n- **`beancount`**: [Beancount](http://furius.ca/beancount/)\n- **`csv`**: [Comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values)\n- **`gnucash-sql`**: [GnuCash](https://www.gnucash.org/) SQL\n- **`ledger`**: [Ledger](https://www.ledger-cli.org/) and [hledger](https://hledger.org/)\n\n## Examples\n\nShow usage information:\n\n```bash\npricehist -h\n```\n```\nusage: pricehist [-h] [--version] [--verbose | --debug]\n                 {sources,source,fetch} ...\n\nFetch historical price data\n\noptional arguments:\n  -h, --help              show this help message and exit\n  --version               show version information\n  --verbose               show all log messages\n\ncommands:\n  {sources,source,fetch}\n    sources               list sources\n    source                show source details\n    fetch                 fetch prices\n```\n\nFetch prices after 2021-01-04, ending 2020-01-15, as CSV:\n\n```bash\npricehist fetch ecb EUR/AUD -sx 2021-01-04 -e 2021-01-15 -o csv\n```\n```\ndate,base,quote,amount,source,type\n2021-01-05,EUR,AUD,1.5927,ecb,reference\n2021-01-06,EUR,AUD,1.5824,ecb,reference\n2021-01-07,EUR,AUD,1.5836,ecb,reference\n2021-01-08,EUR,AUD,1.5758,ecb,reference\n2021-01-11,EUR,AUD,1.5783,ecb,reference\n2021-01-12,EUR,AUD,1.5742,ecb,reference\n2021-01-13,EUR,AUD,1.5734,ecb,reference\n2021-01-14,EUR,AUD,1.5642,ecb,reference\n2021-01-15,EUR,AUD,1.568,ecb,reference\n```\n\nIn Ledger format:\n\n```bash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o ledger\n```\n```\nP 2021-01-04 00:00:00 EUR 1.5928 AUD\nP 2021-01-05 00:00:00 EUR 1.5927 AUD\nP 2021-01-06 00:00:00 EUR 1.5824 AUD\nP 2021-01-07 00:00:00 EUR 1.5836 AUD\nP 2021-01-08 00:00:00 EUR 1.5758 AUD\nP 2021-01-11 00:00:00 EUR 1.5783 AUD\nP 2021-01-12 00:00:00 EUR 1.5742 AUD\nP 2021-01-13 00:00:00 EUR 1.5734 AUD\nP 2021-01-14 00:00:00 EUR 1.5642 AUD\nP 2021-01-15 00:00:00 EUR 1.568 AUD\n```\n\nGenerate SQL for a GnuCash database and apply it immediately:\n\n```bash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | sqlite3 Accounts.gnucash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | mysql -u username -p -D databasename\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | psql -U username -d databasename -v ON_ERROR_STOP=1\n```\n\n## Design choices\n\nTo keep things simple, at least for now, `pricehist` provides only univariate\ntime series of daily historical prices. It doesn't provide other types of\nmarket, financial or economic data, real-time prices, or other temporal\nresolutions. Multiple or multivariate series require multiple invocations.\n\n## Alternatives\n\nBeancount's [`bean-price`](https://beancount.github.io/docs/fetching_prices_in_beancount.html)\ntool fetches historical prices and addresses other workflow concerns in a\nBeancount-specific manner.\n\nThe GnuCash wiki documents [wrapper scripts](https://wiki.gnucash.org/wiki/Stocks/get_prices)\nfor the [Finance::QuoteHist](https://metacpan.org/pod/Finance::QuoteHist) Perl\nmodule.\n\nSome other projects with related goals include:\n* [`hledger-stockquotes`](https://github.com/prikhi/hledger-stockquotes):\n  Generate an HLedger journal containing daily stock quotes for your commodities.\n* [`ledger_get_prices`](https://github.com/nathankot/ledger-get-prices):\n  Uses Yahoo finance to intelligently generate a ledger price database based on your current ledger commodities and time period.\n* [LedgerStockUpdate](https://github.com/adchari/LedgerStockUpdate):\n  Locates any stocks you have in your ledger-cli file, then generates a price database of those stocks.\n* [`market-prices`](https://github.com/barrucadu/hledger-scripts#market-prices):\n  Downloads market values of commodities from a few different sources.\n* [price-database](https://gitlab.com/alensiljak/price-database):\n  A Python library and a CLI for storage of prices.\n",
    'author': 'Chris Berkhout',
    'author_email': 'chris@chrisberkhout.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/chrisberkhout/pricehist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
