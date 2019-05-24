# python-elk-kafka

This python package is developed for Python 3.5 and above 

The purpose is to connect the ELK log system through the kafka message queue, and send the python log information to the ELK platform.

### Installing

`$ pip install python-elk-kafka`

### How to use

Configure logger information via **logging.conf** / **config_dict.py**

The location of the exsample configuration：

config_example/logging.conf or config_example/config_dict.py


#### About ELK, a centralized logging system：(Elasticsearch , Logstash, Kibana)

Elasticsearch is an open source distributed search engine that provides three functions of **collecting**, **analyzing** and **storing** data.

Logstash mainly used as a tool for **collecting**, **analyzing**, and **filtering** logs.

Kibana is a log-analytical **web** interface for Logstash and ElasticSearch that helps **aggregate**, **analyze**, and **search** for important data logs

### Python client to EKL service：

![Image text](imgs/ELK.png)

Message queuing mechanism：

1. Logstash Agent passing the logs to Kafka;

2. Kafka sending the messages in the queue to the specified server where the Logstash is installed;

3. After filtering and analyzing, the data will pass to the Elasticsearch;

4. Finally, Kibana presenting the logs and data to the users.


### Why choose kafka:

The Kafka message queue was uesd, so even if the remote Logstash server stops running due to a failure, the data will be stored first, thus avoiding data loss.


### Project maintenance in this github

_if there have any questions, you can issue or pull request here_