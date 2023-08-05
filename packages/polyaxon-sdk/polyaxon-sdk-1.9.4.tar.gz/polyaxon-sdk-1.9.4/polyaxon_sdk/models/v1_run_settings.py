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


class V1RunSettings(object):
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
        'namespace': 'str',
        'agent': 'V1SettingsCatalog',
        'queue': 'V1SettingsCatalog',
        'artifacts_store': 'V1SettingsCatalog',
        'tensorboard': 'object',
        'build': 'object',
        'component_version': 'V1RunReferenceCatalog',
        'model_versions': 'list[V1RunReferenceCatalog]'
    }

    attribute_map = {
        'namespace': 'namespace',
        'agent': 'agent',
        'queue': 'queue',
        'artifacts_store': 'artifacts_store',
        'tensorboard': 'tensorboard',
        'build': 'build',
        'component_version': 'component_version',
        'model_versions': 'model_versions'
    }

    def __init__(self, namespace=None, agent=None, queue=None, artifacts_store=None, tensorboard=None, build=None, component_version=None, model_versions=None, local_vars_configuration=None):  # noqa: E501
        """V1RunSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespace = None
        self._agent = None
        self._queue = None
        self._artifacts_store = None
        self._tensorboard = None
        self._build = None
        self._component_version = None
        self._model_versions = None
        self.discriminator = None

        if namespace is not None:
            self.namespace = namespace
        if agent is not None:
            self.agent = agent
        if queue is not None:
            self.queue = queue
        if artifacts_store is not None:
            self.artifacts_store = artifacts_store
        if tensorboard is not None:
            self.tensorboard = tensorboard
        if build is not None:
            self.build = build
        if component_version is not None:
            self.component_version = component_version
        if model_versions is not None:
            self.model_versions = model_versions

    @property
    def namespace(self):
        """Gets the namespace of this V1RunSettings.  # noqa: E501


        :return: The namespace of this V1RunSettings.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this V1RunSettings.


        :param namespace: The namespace of this V1RunSettings.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def agent(self):
        """Gets the agent of this V1RunSettings.  # noqa: E501


        :return: The agent of this V1RunSettings.  # noqa: E501
        :rtype: V1SettingsCatalog
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this V1RunSettings.


        :param agent: The agent of this V1RunSettings.  # noqa: E501
        :type: V1SettingsCatalog
        """

        self._agent = agent

    @property
    def queue(self):
        """Gets the queue of this V1RunSettings.  # noqa: E501


        :return: The queue of this V1RunSettings.  # noqa: E501
        :rtype: V1SettingsCatalog
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this V1RunSettings.


        :param queue: The queue of this V1RunSettings.  # noqa: E501
        :type: V1SettingsCatalog
        """

        self._queue = queue

    @property
    def artifacts_store(self):
        """Gets the artifacts_store of this V1RunSettings.  # noqa: E501


        :return: The artifacts_store of this V1RunSettings.  # noqa: E501
        :rtype: V1SettingsCatalog
        """
        return self._artifacts_store

    @artifacts_store.setter
    def artifacts_store(self, artifacts_store):
        """Sets the artifacts_store of this V1RunSettings.


        :param artifacts_store: The artifacts_store of this V1RunSettings.  # noqa: E501
        :type: V1SettingsCatalog
        """

        self._artifacts_store = artifacts_store

    @property
    def tensorboard(self):
        """Gets the tensorboard of this V1RunSettings.  # noqa: E501


        :return: The tensorboard of this V1RunSettings.  # noqa: E501
        :rtype: object
        """
        return self._tensorboard

    @tensorboard.setter
    def tensorboard(self, tensorboard):
        """Sets the tensorboard of this V1RunSettings.


        :param tensorboard: The tensorboard of this V1RunSettings.  # noqa: E501
        :type: object
        """

        self._tensorboard = tensorboard

    @property
    def build(self):
        """Gets the build of this V1RunSettings.  # noqa: E501


        :return: The build of this V1RunSettings.  # noqa: E501
        :rtype: object
        """
        return self._build

    @build.setter
    def build(self, build):
        """Sets the build of this V1RunSettings.


        :param build: The build of this V1RunSettings.  # noqa: E501
        :type: object
        """

        self._build = build

    @property
    def component_version(self):
        """Gets the component_version of this V1RunSettings.  # noqa: E501


        :return: The component_version of this V1RunSettings.  # noqa: E501
        :rtype: V1RunReferenceCatalog
        """
        return self._component_version

    @component_version.setter
    def component_version(self, component_version):
        """Sets the component_version of this V1RunSettings.


        :param component_version: The component_version of this V1RunSettings.  # noqa: E501
        :type: V1RunReferenceCatalog
        """

        self._component_version = component_version

    @property
    def model_versions(self):
        """Gets the model_versions of this V1RunSettings.  # noqa: E501


        :return: The model_versions of this V1RunSettings.  # noqa: E501
        :rtype: list[V1RunReferenceCatalog]
        """
        return self._model_versions

    @model_versions.setter
    def model_versions(self, model_versions):
        """Sets the model_versions of this V1RunSettings.


        :param model_versions: The model_versions of this V1RunSettings.  # noqa: E501
        :type: list[V1RunReferenceCatalog]
        """

        self._model_versions = model_versions

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
        if not isinstance(other, V1RunSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1RunSettings):
            return True

        return self.to_dict() != other.to_dict()
