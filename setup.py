# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='python-elk-kafka',
    version='0.0.1',
    description=('A python3 elk project use kafka to send messages'),
    url='https://github.com/kep-w/python-elk-kafka',
    author='Kepner Wu',
    author_email='kepner_wu@hotmail.com',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='elk python3 kafka logstash',
    install_requires = [
        'kafka-python==0.9.5',
    ],
)