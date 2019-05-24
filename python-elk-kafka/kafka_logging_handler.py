# -*- coding:utf-8 -*-

"""
Auther: Kepner Wu
Mail: kepner_wu@hotmail.com
Important Info: avoid naming the logger as kafka in your config document, it will be droped to avoid infinite recursion
"""

import socket
import datetime
import traceback as tb
import logging
import json
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, KeyedProducer
from kafka.conn import DEFAULT_SOCKET_TIMEOUT_SECONDS


class KafkaLoggingHandler(logging.Handler):
    """
    Use kafka to send msg to elk platform
    """

    def __init__(self, hosts_list, topic,
                 timeout_secs=DEFAULT_SOCKET_TIMEOUT_SECONDS, **kwargs):
        logging.Handler.__init__(self)

        self.kafka_client = KafkaClient(hosts_list, timeout=timeout_secs)
        self.key = kwargs.get("key", None)
        self.kafka_topic_name = topic

        if not self.key:
            self.producer = SimpleProducer(self.kafka_client, **kwargs)
        else:
            self.producer = KeyedProducer(self.kafka_client, **kwargs)

    def emit(self, record):
        """
        emit record
        :param record:
        :return:
        """
        # drop kafka logging to avoid infinite recursion
        if record.name == 'kafka':
            return
        try:
            # use default formatting
            msg = self.format(record)
            msg = msg.encode("utf-8")
            # produce message
            if not self.key:
                self.producer.send_messages(self.kafka_topic_name, msg)
            else:
                self.producer.send_messages(
                    self.kafka_topic_name, self.key, msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)

    def close(self):
        """
        close the client
        :return:
        """
        if self.producer is not None:
            self.producer.stop()
        logging.Handler.close(self)


class LogstashFormatter(logging.Formatter):
    """
    A custom formatter to prepare logs to be shipped out to logstash.
    """

    def __init__(self,
                 fmt=None,
                 datefmt=None,
                 style=None):
        """
        :param fmt: Config as a JSON string, allowed fields;
               extra: provide extra fields always present in logs
               source_host: override source host name
        :param datefmt: Date format to use (required by logging.Formatter
            interface but not used)
        :param style: JSON encoder to forward to json.dumps
        :param json_default: Default JSON representation for unknown types,
                             by default coerce everything to a string
        """

        if fmt is not None:
            self._fmt = json.loads(fmt)
        else:
            self._fmt = {}
        self.style = style
        if 'extra' not in self._fmt:
            self.defaults = {}
        else:
            self.defaults = self._fmt['extra']
        if 'source_host' in self._fmt:
            self.source_host = self._fmt['source_host']
        else:
            try:
                self.source_host = socket.gethostname()
            except BaseException:
                self.source_host = ""

    def format(self, record):
        """
        Format a log record to JSON, if the message is a dict
        assume an empty message and use the dict as additional
        fields.
        """

        fields = record.__dict__.copy()

        if isinstance(record.msg, dict):
            fields.update(record.msg)
            fields.pop('msg')
            msg = ""
        else:
            msg = record.getMessage()

        if 'msg' in fields:
            fields.pop('msg')

        if 'exc_info' in fields:
            if fields['exc_info']:
                formatted = tb.format_exception(*fields['exc_info'])
                fields['exception'] = formatted
            fields.pop('exc_info')

        if 'exc_text' in fields and not fields['exc_text']:
            fields.pop('exc_text')

        logr = self.defaults.copy()

        logr.update({**{'message': msg,
                        '@timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'source_host': self.source_host},
                     **self._build_fields(logr, fields)})
        # in logging module style defaults value is "%" , so here need to
        # change defaults to None
        self.style = None if self.style == "%" else self.style
        return json.dumps(logr, cls=self.style)

    def _build_fields(self, defaults, fields):
        """
        Return necessary fields chose from defaults
        :param defaults: logr from
        :param fields:
        :return:
        """
        necessary = dict()
        fields = {**defaults.get('@fields', {}), **fields}
        try:
            necessary['logger'] = "path:{} - module:{} - lineno:{}".format(fields.get('pathname', None), fields.get(
                'module', None), fields.get('lineno', None))
            necessary['level'] = fields.get('levelname', None)
            necessary['process'] = "process_name:{} - process:{}".format(
                fields.get('processName', None), fields.get('process', None))
            necessary['thread'] = "thread_name:{} - thread:{}".format(
                fields.get('threadName', None), fields.get('thread', None))
        except BaseException:
            necessary = fields
        return necessary
