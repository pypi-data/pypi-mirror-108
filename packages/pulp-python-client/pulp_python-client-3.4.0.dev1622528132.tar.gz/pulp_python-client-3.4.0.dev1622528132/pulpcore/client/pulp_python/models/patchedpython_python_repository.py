# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_python.configuration import Configuration


class PatchedpythonPythonRepository(object):
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
        'pulp_labels': 'object',
        'name': 'str',
        'description': 'str',
        'retained_versions': 'int',
        'remote': 'str',
        'autopublish': 'bool'
    }

    attribute_map = {
        'pulp_labels': 'pulp_labels',
        'name': 'name',
        'description': 'description',
        'retained_versions': 'retained_versions',
        'remote': 'remote',
        'autopublish': 'autopublish'
    }

    def __init__(self, pulp_labels=None, name=None, description=None, retained_versions=None, remote=None, autopublish=False, local_vars_configuration=None):  # noqa: E501
        """PatchedpythonPythonRepository - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_labels = None
        self._name = None
        self._description = None
        self._retained_versions = None
        self._remote = None
        self._autopublish = None
        self.discriminator = None

        if pulp_labels is not None:
            self.pulp_labels = pulp_labels
        if name is not None:
            self.name = name
        self.description = description
        self.retained_versions = retained_versions
        self.remote = remote
        if autopublish is not None:
            self.autopublish = autopublish

    @property
    def pulp_labels(self):
        """Gets the pulp_labels of this PatchedpythonPythonRepository.  # noqa: E501


        :return: The pulp_labels of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: object
        """
        return self._pulp_labels

    @pulp_labels.setter
    def pulp_labels(self, pulp_labels):
        """Sets the pulp_labels of this PatchedpythonPythonRepository.


        :param pulp_labels: The pulp_labels of this PatchedpythonPythonRepository.  # noqa: E501
        :type: object
        """

        self._pulp_labels = pulp_labels

    @property
    def name(self):
        """Gets the name of this PatchedpythonPythonRepository.  # noqa: E501

        A unique name for this repository.  # noqa: E501

        :return: The name of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedpythonPythonRepository.

        A unique name for this repository.  # noqa: E501

        :param name: The name of this PatchedpythonPythonRepository.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this PatchedpythonPythonRepository.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PatchedpythonPythonRepository.

        An optional description.  # noqa: E501

        :param description: The description of this PatchedpythonPythonRepository.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def retained_versions(self):
        """Gets the retained_versions of this PatchedpythonPythonRepository.  # noqa: E501

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :return: The retained_versions of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: int
        """
        return self._retained_versions

    @retained_versions.setter
    def retained_versions(self, retained_versions):
        """Sets the retained_versions of this PatchedpythonPythonRepository.

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :param retained_versions: The retained_versions of this PatchedpythonPythonRepository.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                retained_versions is not None and retained_versions < 1):  # noqa: E501
            raise ValueError("Invalid value for `retained_versions`, must be a value greater than or equal to `1`")  # noqa: E501

        self._retained_versions = retained_versions

    @property
    def remote(self):
        """Gets the remote of this PatchedpythonPythonRepository.  # noqa: E501


        :return: The remote of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: str
        """
        return self._remote

    @remote.setter
    def remote(self, remote):
        """Sets the remote of this PatchedpythonPythonRepository.


        :param remote: The remote of this PatchedpythonPythonRepository.  # noqa: E501
        :type: str
        """

        self._remote = remote

    @property
    def autopublish(self):
        """Gets the autopublish of this PatchedpythonPythonRepository.  # noqa: E501

        Whether to automatically create publications for new repository versions, and update any distributions pointing to this repository.  # noqa: E501

        :return: The autopublish of this PatchedpythonPythonRepository.  # noqa: E501
        :rtype: bool
        """
        return self._autopublish

    @autopublish.setter
    def autopublish(self, autopublish):
        """Sets the autopublish of this PatchedpythonPythonRepository.

        Whether to automatically create publications for new repository versions, and update any distributions pointing to this repository.  # noqa: E501

        :param autopublish: The autopublish of this PatchedpythonPythonRepository.  # noqa: E501
        :type: bool
        """

        self._autopublish = autopublish

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
        if not isinstance(other, PatchedpythonPythonRepository):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedpythonPythonRepository):
            return True

        return self.to_dict() != other.to_dict()
