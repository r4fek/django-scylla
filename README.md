# Django Scylla - the Cassandra & ScyllaDB backend for Django

Django-scylla makes possible to connect your Django app to Cassandra or ScyllaDB and **use native Django ORM** as with any other relational database backend.


[![Latest version](https://img.shields.io/pypi/v/django-scylla.svg "Latest version")](https://pypi.python.org/pypi/django-scylla/)
![workflow](https://github.com/r4fek/django-scylla/actions/workflows/tox.yml/badge.svg)

Discord: https://discord.gg/pxunMGmDNc

## Sponsors ##
Help support ongoing development and maintenance by [sponsoring Django Scylla](https://github.com/sponsors/r4fek).

## Installation ##

Recommended installation:

    pip install django-scylla

## Basic Usage ##

1. Add `django_scylla` to `INSTALLED_APPS` in your `settings.py` file:

        INSTALLED_APPS = ('django_scylla',) + INSTALLED_APPS

2. Change `DATABASES` setting:

        DATABASES = {
            'default': {
                'ENGINE': 'django_scylla',
                'NAME': 'db',
                'TEST_NAME': 'test_db',
                'HOST': 'db1.example.com,db2.example.com,db3.example.com',
                'OPTIONS': {
                    'replication': {
                        'strategy_class': ...,
                        'replication_factor': ...
                    },
                    'execution_profile': {
                        'load_balancing_policy': ...,
                        'retry_policy': ...,
                        'consistency_level': ...,
                        'serial_consistency_level': ...,
                        'request_timeout': ...,
                        'speculative_execution_policy': ...
                    }
                    'connection': {
                        # Full list of connection options can be found here: https://docs.datastax.com/en/developer/python-driver/3.26/api/cassandra/cluster/
                        'cql_version': ...,
                        'protocol_version': ...
                        'compression': ...,
                        'consistency': ...,
                        'lazy_connect': ...,
                        'retry_connect': ...,
                    }
                }
            }
        }

3. Define some model:

        # myapp/models.py

        from django.db import models


        class Person(models.Model):
            first_name = models.CharField(max_length=30)
            last_name = models.CharField(max_length=30)


4. Connect to ScyllaDB and create a keyspace.
5. Run `./manage.py makemigrations && ./manage.py migrate`
6. Done!

## License ##
Copyright (c) 2021-2022, [Rafał Furmański](https://linkedin.com/in/furmanski).

All rights reserved. Licensed under MIT License.
