# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['containerlog', 'containerlog.proxy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'containerlog',
    'version': '0.4.0',
    'description': 'Optimized, opinionated structured logging for Python',
    'long_description': "# containerlog\n\nA lightweight, optimized, and opinionated structured logging library for Python, intended for containerized applications.\n\n`containerlog` was born out of a desire to have high-quality structured logging for\ncontainerized applications (e.g. microservices) without having to compromise detailed\nlogging for application/request latency.\n\n[`structlog`](https://www.structlog.org/en/stable/) is a great general-purpose structured\nlogging library for Python, but being general-purpose means that there is additional overhead\nwhen logging messages.\n\nWhen [we](https://github.com/vapor-ware) updated a microservice to use structured logging,\nwe found that [request latency went up](https://github.com/vapor-ware/synse-server/issues/384),\nseemingly due to the transition to use `structlog`.\n\n`containerlog` is not for everyone. It is highly opinionated, minimally configurable,\nand intentionally feature-sparse so that it can achieve [better performance](#benchmarks) than\nthe Python standard logger\n\nNot every application needs optimized logging, but where latency and performance matters,\n`containerlog` could work for you.\n\n```\ntimestamp='2020-07-23T13:11:28.009804Z' logger='my-logger' level='debug' event='loading configuration' path='./config.yaml'\ntimestamp='2020-07-23T13:11:28.010137Z' logger='my-logger' level='info' event='starting application'\ntimestamp='2020-07-23T13:11:28.010158Z' logger='my-logger' level='warn' event='having too much fun' countdown=[3, 2, 1]\n```\n\n## Installation\n\n`containerlog` can be installed with pip:\n\n```\npip install containerlog\n```\n\nIt is only intended to work for Python 3.6+.\n\n## Usage\n\nSee the documentation at https://containerlog.readthedocs.io/en/latest/\n\n## Optimizations\n\nThere are numerous sources discussion micro-optimizations in Python. This project probably\ndoes not implement them all, so there is room for improvement. Current optimization work has\nleveraged:\n\n* [`dis`](https://docs.python.org/3/library/dis.html): to disassemble python bytecode for analysis\n* [`timeit`](https://docs.python.org/3/library/timeit.html): to measure execution time of code snippets\n\nIf you wish to contribute optimizations and use other libraries, tools, or sources, open a PR to add\nthem to this list.\n\n## Benchmarks\n\nBenchmarking scripts can be found in the [benchmarks](benchmarks) directory. To run,\n\n```\n$ cd benchmarks\n$ ./run.sh\n```\n\nThis will run benchmarks the Python standard logger and for `containerlog`. The latest results\ncan be found below.\n\n### Results\n\nBenchmarks were measured using Python 3.8.0 on macOS 10.15.1 with a 2.9 GHz 6-Core Intel Core i9\nprocessor and 16 GB 2400 MHz DDR4 memory.\n\n![containerlog 0.3.0](benchmarks/results/benchmark-containerlog-0.3.0.png)\n\n| Benchmark | std logger (ns) | std proxy (ns) | containerlog (ns) |\n| --------- | --------------- | -------------- | ----------------- |\n| baseline | 0.68 +/- 0.02 | 0.69 +/- 0.01 | 0.7 +/- 0.02 |\n| silent | 108.0 +/- 6.0 | 1140.0 +/- 50.0 | 51.7 +/- 1.7 |\n| basic | 4750.0 +/- 160.0 | 1140.0 +/- 60.0 | 1070.0 +/- 50.0 |\n| short-simple | 5370.0 +/- 160.0 | 1280.0 +/- 60.0 | 1330.0 +/- 60.0 |\n| long-simple | 5280.0 +/- 180.0 | 1480.0 +/- 70.0 | 2120.0 +/- 60.0 |\n| short-complex | 5630.0 +/- 170.0 | 1500.0 +/- 150.0 | 1480.0 +/- 80.0 |\n| long-complex | 6900.0 +/- 190.0 | 2870.0 +/- 80.0 | 3260.0 +/- 80.0 |\n| exception | 10400.0 +/- 300.0 | 4440.0 +/- 150.0 | 4370.0 +/- 500.0 |\n\n## Contribute\n\nWhile `containerlog` is intentionally feature-sparse, feature requests are welcome. Additionally,\nif you can find any other ways to micro-optimize the codebase, pull requests are very much\nappreciated.\n",
    'author': 'Erick Daniszewski',
    'author_email': 'erick@vapor.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vapor-ware/containerlog',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
