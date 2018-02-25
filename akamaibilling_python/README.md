# Akamai Billing API Client

This module communicates with the Akamai APIs to get information about usage
of all contracts it its belonging reporting groups

## Requirements

This client as several requirements:

- Docker
- Python 3.6
- MySQL Database

## Description of components

### Docker

You can run the *Akamai Billing API Client* as a standalone application or in a docker container. Docker is used to run this the *Akamai Billing API Client* on AWS Batch.
You can build the docker container with following command:

```bash
cd /PATH/TO/PROJECT/DIRECTORY
docker build -t NICE_NAME:TAG_NAME .
```

### Python

*Akamai Billing API Client* is written in Python 3.6 an is not backward compatible to Python 2.x

### MySQL

The *Akamai Billing API Client* saves received data from the Akamai APIs into a MySQL Database.
