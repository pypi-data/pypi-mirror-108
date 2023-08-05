# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['knada_kafka_consumer',
 'knada_kafka_consumer.bq',
 'knada_kafka_consumer.consumer',
 'knada_kafka_consumer.kafka']

package_data = \
{'': ['*']}

install_requires = \
['avro-python3>=1.10.1,<2.0.0',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.61.1,<0.62.0',
 'google-api-core>=1.22.2,<2.0.0',
 'google-auth>=1.22.0,<2.0.0',
 'google-cloud-bigquery>=2.1.0,<3.0.0',
 'google-cloud-core>=1.4.1,<2.0.0',
 'google-cloud-storage>=1.31.2,<2.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'kafka-python>=2.0.2,<3.0.0',
 'prometheus_client>=0.9.0,<0.10.0',
 'pytest>=6.2.1,<7.0.0',
 'uvicorn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'knada-kafka-consumer',
    'version': '0.1.10',
    'description': '',
    'long_description': None,
    'author': 'NAV IT dataplattform',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
