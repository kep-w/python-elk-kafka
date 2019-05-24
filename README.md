## python-elk-kafka

此模块针对Python3.5 及以上版本

实现通过kafka连接elk日志系统，将Python程序中的日志信息发送到ELK平台。

#### 关于ELK, 一个集中式日志系统：(Elasticsearch , Logstash, Kibana)

Elasticsearch是个开源分布式搜索引擎，提供搜集、分析、存储数据三大功能。

Logstash 主要是用来日志的搜集、分析、过滤日志的工具，支持大量的数据获取方式。

Kibana 为 Logstash 和 ElasticSearch 提供的日志分析友好的 Web 界面，可以帮助汇总、分析和搜索重要数据日志

#### 从Python到EKL使用架构：

![Image text](imgs/ELK.png)

通过消息队列机制：

1.Logstash Agent先将日志传递给Kafka

2.kafka将队列中消息或数据传递给Logstash

3.Logstash过滤、分析后将数据传递给Elasticsearch存储

4.最后由Kibana将日志和数据呈现给用户

优势： 引入了Kafka,所以即使远端Logstash server因故障停止运行，数据将会先被存储下来，从而避免数据丢失。
