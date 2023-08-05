# coding: utf-8

"""
    ELEMENTS API

    The version of the OpenAPI document: 2
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from elements_sdk.configuration import Configuration


class ClientsEndpointResponse(object):
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
        'version': 'str',
        'full_version': 'str',
        'platform': 'str',
        'file': 'str'
    }

    attribute_map = {
        'version': 'version',
        'full_version': 'full_version',
        'platform': 'platform',
        'file': 'file'
    }

    def __init__(self, version=None, full_version=None, platform=None, file=None, local_vars_configuration=None):  # noqa: E501
        """ClientsEndpointResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._full_version = None
        self._platform = None
        self._file = None
        self.discriminator = None

        self.version = version
        self.full_version = full_version
        self.platform = platform
        self.file = file

    @property
    def version(self):
        """Gets the version of this ClientsEndpointResponse.  # noqa: E501


        :return: The version of this ClientsEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ClientsEndpointResponse.


        :param version: The version of this ClientsEndpointResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                version is not None and len(version) < 1):
            raise ValueError("Invalid value for `version`, length must be greater than or equal to `1`")  # noqa: E501

        self._version = version

    @property
    def full_version(self):
        """Gets the full_version of this ClientsEndpointResponse.  # noqa: E501


        :return: The full_version of this ClientsEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._full_version

    @full_version.setter
    def full_version(self, full_version):
        """Sets the full_version of this ClientsEndpointResponse.


        :param full_version: The full_version of this ClientsEndpointResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and full_version is None:  # noqa: E501
            raise ValueError("Invalid value for `full_version`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                full_version is not None and len(full_version) < 1):
            raise ValueError("Invalid value for `full_version`, length must be greater than or equal to `1`")  # noqa: E501

        self._full_version = full_version

    @property
    def platform(self):
        """Gets the platform of this ClientsEndpointResponse.  # noqa: E501


        :return: The platform of this ClientsEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this ClientsEndpointResponse.


        :param platform: The platform of this ClientsEndpointResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and platform is None:  # noqa: E501
            raise ValueError("Invalid value for `platform`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                platform is not None and len(platform) < 1):
            raise ValueError("Invalid value for `platform`, length must be greater than or equal to `1`")  # noqa: E501

        self._platform = platform

    @property
    def file(self):
        """Gets the file of this ClientsEndpointResponse.  # noqa: E501


        :return: The file of this ClientsEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this ClientsEndpointResponse.


        :param file: The file of this ClientsEndpointResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and file is None:  # noqa: E501
            raise ValueError("Invalid value for `file`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                file is not None and len(file) < 1):
            raise ValueError("Invalid value for `file`, length must be greater than or equal to `1`")  # noqa: E501

        self._file = file

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
        if not isinstance(other, ClientsEndpointResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClientsEndpointResponse):
            return True

        return self.to_dict() != other.to_dict()
