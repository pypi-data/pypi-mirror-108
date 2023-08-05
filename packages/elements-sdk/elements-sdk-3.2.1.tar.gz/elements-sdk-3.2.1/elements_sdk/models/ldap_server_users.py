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


class LDAPServerUsers(object):
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
        'users': 'list[LDAPServerUser]'
    }

    attribute_map = {
        'users': 'users'
    }

    def __init__(self, users=None, local_vars_configuration=None):  # noqa: E501
        """LDAPServerUsers - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._users = None
        self.discriminator = None

        self.users = users

    @property
    def users(self):
        """Gets the users of this LDAPServerUsers.  # noqa: E501


        :return: The users of this LDAPServerUsers.  # noqa: E501
        :rtype: list[LDAPServerUser]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this LDAPServerUsers.


        :param users: The users of this LDAPServerUsers.  # noqa: E501
        :type: list[LDAPServerUser]
        """
        if self.local_vars_configuration.client_side_validation and users is None:  # noqa: E501
            raise ValueError("Invalid value for `users`, must not be `None`")  # noqa: E501

        self._users = users

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
        if not isinstance(other, LDAPServerUsers):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LDAPServerUsers):
            return True

        return self.to_dict() != other.to_dict()
