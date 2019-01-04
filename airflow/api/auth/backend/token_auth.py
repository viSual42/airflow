# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from functools import wraps
from flask import request
from airflow import configuration as conf
from flask import Response
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log

client_auth = None
_TOKEN = None

def init_app(app):
    global _TOKEN
    _TOKEN = conf.get('api', 'api_key')
    #log.info("Token set %s", _TOKEN)
    


def requires_authentication(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        header = request.headers.get("Authorization")
        if header:
            #log.info("Header from request %s", header)
            token = ''.join(header.split()[1:])
            #log.info("Token from request %s", token)
            if token == _TOKEN:
                return function(*args, **kwargs)
            else:
                return _forbidden()
        return _unauthorized()
    return decorated


def _unauthorized():
    """
    Indicate that authorization is required
    :return:
    """
    return Response("Unauthorized", 401, {"WWW-Authenticate": "Negotiate"})


def _forbidden():
    return Response("Forbidden", 403)