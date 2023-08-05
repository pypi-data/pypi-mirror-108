#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.9.4
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1Dask(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'kind': 'str',
        'threads': 'int',
        'scale': 'int',
        'adapt_min': 'int',
        'adapt_max': 'int',
        'adapt_interval': 'str',
        'environment': 'V1Environment',
        'connections': 'list[str]',
        'volumes': 'list[V1Volume]',
        'init': 'list[V1Init]',
        'sidecars': 'list[V1Container]',
        'container': 'V1Container'
    }

    attribute_map = {
        'kind': 'kind',
        'threads': 'threads',
        'scale': 'scale',
        'adapt_min': 'adaptMin',
        'adapt_max': 'adaptMax',
        'adapt_interval': 'adaptInterval',
        'environment': 'environment',
        'connections': 'connections',
        'volumes': 'volumes',
        'init': 'init',
        'sidecars': 'sidecars',
        'container': 'container'
    }

    def __init__(self, kind='dask', threads=None, scale=None, adapt_min=None, adapt_max=None, adapt_interval=None, environment=None, connections=None, volumes=None, init=None, sidecars=None, container=None, local_vars_configuration=None):  # noqa: E501
        """V1Dask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._kind = None
        self._threads = None
        self._scale = None
        self._adapt_min = None
        self._adapt_max = None
        self._adapt_interval = None
        self._environment = None
        self._connections = None
        self._volumes = None
        self._init = None
        self._sidecars = None
        self._container = None
        self.discriminator = None

        if kind is not None:
            self.kind = kind
        if threads is not None:
            self.threads = threads
        if scale is not None:
            self.scale = scale
        if adapt_min is not None:
            self.adapt_min = adapt_min
        if adapt_max is not None:
            self.adapt_max = adapt_max
        if adapt_interval is not None:
            self.adapt_interval = adapt_interval
        if environment is not None:
            self.environment = environment
        if connections is not None:
            self.connections = connections
        if volumes is not None:
            self.volumes = volumes
        if init is not None:
            self.init = init
        if sidecars is not None:
            self.sidecars = sidecars
        if container is not None:
            self.container = container

    @property
    def kind(self):
        """Gets the kind of this V1Dask.  # noqa: E501


        :return: The kind of this V1Dask.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1Dask.


        :param kind: The kind of this V1Dask.  # noqa: E501
        :type: str
        """

        self._kind = kind

    @property
    def threads(self):
        """Gets the threads of this V1Dask.  # noqa: E501


        :return: The threads of this V1Dask.  # noqa: E501
        :rtype: int
        """
        return self._threads

    @threads.setter
    def threads(self, threads):
        """Sets the threads of this V1Dask.


        :param threads: The threads of this V1Dask.  # noqa: E501
        :type: int
        """

        self._threads = threads

    @property
    def scale(self):
        """Gets the scale of this V1Dask.  # noqa: E501


        :return: The scale of this V1Dask.  # noqa: E501
        :rtype: int
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        """Sets the scale of this V1Dask.


        :param scale: The scale of this V1Dask.  # noqa: E501
        :type: int
        """

        self._scale = scale

    @property
    def adapt_min(self):
        """Gets the adapt_min of this V1Dask.  # noqa: E501


        :return: The adapt_min of this V1Dask.  # noqa: E501
        :rtype: int
        """
        return self._adapt_min

    @adapt_min.setter
    def adapt_min(self, adapt_min):
        """Sets the adapt_min of this V1Dask.


        :param adapt_min: The adapt_min of this V1Dask.  # noqa: E501
        :type: int
        """

        self._adapt_min = adapt_min

    @property
    def adapt_max(self):
        """Gets the adapt_max of this V1Dask.  # noqa: E501


        :return: The adapt_max of this V1Dask.  # noqa: E501
        :rtype: int
        """
        return self._adapt_max

    @adapt_max.setter
    def adapt_max(self, adapt_max):
        """Sets the adapt_max of this V1Dask.


        :param adapt_max: The adapt_max of this V1Dask.  # noqa: E501
        :type: int
        """

        self._adapt_max = adapt_max

    @property
    def adapt_interval(self):
        """Gets the adapt_interval of this V1Dask.  # noqa: E501


        :return: The adapt_interval of this V1Dask.  # noqa: E501
        :rtype: str
        """
        return self._adapt_interval

    @adapt_interval.setter
    def adapt_interval(self, adapt_interval):
        """Sets the adapt_interval of this V1Dask.


        :param adapt_interval: The adapt_interval of this V1Dask.  # noqa: E501
        :type: str
        """

        self._adapt_interval = adapt_interval

    @property
    def environment(self):
        """Gets the environment of this V1Dask.  # noqa: E501


        :return: The environment of this V1Dask.  # noqa: E501
        :rtype: V1Environment
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this V1Dask.


        :param environment: The environment of this V1Dask.  # noqa: E501
        :type: V1Environment
        """

        self._environment = environment

    @property
    def connections(self):
        """Gets the connections of this V1Dask.  # noqa: E501


        :return: The connections of this V1Dask.  # noqa: E501
        :rtype: list[str]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """Sets the connections of this V1Dask.


        :param connections: The connections of this V1Dask.  # noqa: E501
        :type: list[str]
        """

        self._connections = connections

    @property
    def volumes(self):
        """Gets the volumes of this V1Dask.  # noqa: E501

        Volumes is a list of volumes that can be mounted.  # noqa: E501

        :return: The volumes of this V1Dask.  # noqa: E501
        :rtype: list[V1Volume]
        """
        return self._volumes

    @volumes.setter
    def volumes(self, volumes):
        """Sets the volumes of this V1Dask.

        Volumes is a list of volumes that can be mounted.  # noqa: E501

        :param volumes: The volumes of this V1Dask.  # noqa: E501
        :type: list[V1Volume]
        """

        self._volumes = volumes

    @property
    def init(self):
        """Gets the init of this V1Dask.  # noqa: E501


        :return: The init of this V1Dask.  # noqa: E501
        :rtype: list[V1Init]
        """
        return self._init

    @init.setter
    def init(self, init):
        """Sets the init of this V1Dask.


        :param init: The init of this V1Dask.  # noqa: E501
        :type: list[V1Init]
        """

        self._init = init

    @property
    def sidecars(self):
        """Gets the sidecars of this V1Dask.  # noqa: E501


        :return: The sidecars of this V1Dask.  # noqa: E501
        :rtype: list[V1Container]
        """
        return self._sidecars

    @sidecars.setter
    def sidecars(self, sidecars):
        """Sets the sidecars of this V1Dask.


        :param sidecars: The sidecars of this V1Dask.  # noqa: E501
        :type: list[V1Container]
        """

        self._sidecars = sidecars

    @property
    def container(self):
        """Gets the container of this V1Dask.  # noqa: E501


        :return: The container of this V1Dask.  # noqa: E501
        :rtype: V1Container
        """
        return self._container

    @container.setter
    def container(self, container):
        """Sets the container of this V1Dask.


        :param container: The container of this V1Dask.  # noqa: E501
        :type: V1Container
        """

        self._container = container

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Dask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Dask):
            return True

        return self.to_dict() != other.to_dict()
