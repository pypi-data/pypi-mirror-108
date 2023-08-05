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


class Download(object):
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
        'id': 'int',
        'name': 'str',
        'icon_path': 'str',
        'fa_icon': 'str',
        'path': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'icon_path': 'icon_path',
        'fa_icon': 'fa_icon',
        'path': 'path'
    }

    def __init__(self, id=None, name=None, icon_path=None, fa_icon=None, path=None, local_vars_configuration=None):  # noqa: E501
        """Download - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._icon_path = None
        self._fa_icon = None
        self._path = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.icon_path = icon_path
        self.fa_icon = fa_icon
        self.path = path

    @property
    def id(self):
        """Gets the id of this Download.  # noqa: E501


        :return: The id of this Download.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Download.


        :param id: The id of this Download.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Download.  # noqa: E501


        :return: The name of this Download.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Download.


        :param name: The name of this Download.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 255):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def icon_path(self):
        """Gets the icon_path of this Download.  # noqa: E501


        :return: The icon_path of this Download.  # noqa: E501
        :rtype: str
        """
        return self._icon_path

    @icon_path.setter
    def icon_path(self, icon_path):
        """Sets the icon_path of this Download.


        :param icon_path: The icon_path of this Download.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                icon_path is not None and len(icon_path) > 255):
            raise ValueError("Invalid value for `icon_path`, length must be less than or equal to `255`")  # noqa: E501

        self._icon_path = icon_path

    @property
    def fa_icon(self):
        """Gets the fa_icon of this Download.  # noqa: E501


        :return: The fa_icon of this Download.  # noqa: E501
        :rtype: str
        """
        return self._fa_icon

    @fa_icon.setter
    def fa_icon(self, fa_icon):
        """Sets the fa_icon of this Download.


        :param fa_icon: The fa_icon of this Download.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                fa_icon is not None and len(fa_icon) > 255):
            raise ValueError("Invalid value for `fa_icon`, length must be less than or equal to `255`")  # noqa: E501

        self._fa_icon = fa_icon

    @property
    def path(self):
        """Gets the path of this Download.  # noqa: E501


        :return: The path of this Download.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this Download.


        :param path: The path of this Download.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and path is None:  # noqa: E501
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) > 255):
            raise ValueError("Invalid value for `path`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) < 1):
            raise ValueError("Invalid value for `path`, length must be greater than or equal to `1`")  # noqa: E501

        self._path = path

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
        if not isinstance(other, Download):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Download):
            return True

        return self.to_dict() != other.to_dict()
