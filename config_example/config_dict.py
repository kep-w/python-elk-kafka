
logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'kibana': {
            'class': 'python-elk-kafka.LogstashFormatter',
            'format': '{"extra":{"app_name":"myPythonApp", "log_type":"your log type"}}'
        },
    },
    'handlers': {
        'error_kibana': {
            'class': 'python-elk-kafka.KafkaLoggingHandler',
            'level': 'ERROR',
            'formatter': 'kibana',
            'hosts_list':"kafka-srv1:port, kafka-srv2:port, kafka-srv3:port",
            'topic': 'your topic',
        },
        'warn_kibana': {
            'class': 'python-elk-kafka.KafkaLoggingHandler',
            'level': 'WARN',
            'formatter': 'kibana',
            'hosts_list':"kafka-srv1:port, kafka-srv2:port, kafka-srv3:port",
            'topic': 'your topic',
        },
        'info_kibana': {
            'class': 'python-elk-kafka.KafkaLoggingHandler',
            'level': 'INFO',
            'formatter': 'kibana',
            'hosts_list':"kafka-srv1:port, kafka-srv2:port, kafka-srv3:port",
            'topic': 'your topic',
        },
        'debug_kibana': {
            'class': 'python-elk-kafka.KafkaLoggingHandler',
            'level': 'DEBUG',
            'formatter': 'kibana',
            'hosts_list':"kafka-srv1:port, kafka-srv2:port, kafka-srv3:port",
            'topic': 'your topic',
        }
    },
    'loggers': {
        'kibana_logger': {
            'handlers': ['debug_kibana', 'info_kibana', 'warn_kibana', 'error_kibana'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
