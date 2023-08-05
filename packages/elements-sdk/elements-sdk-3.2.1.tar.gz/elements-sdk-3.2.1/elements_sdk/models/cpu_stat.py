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


class CPUStat(object):
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
        'time': 'float',
        'c_idle': 'float',
        'c_iowait': 'float',
        'c_system': 'float',
        'c_user': 'float',
        'c_usage': 'float'
    }

    attribute_map = {
        'time': 'time',
        'c_idle': 'c_idle',
        'c_iowait': 'c_iowait',
        'c_system': 'c_system',
        'c_user': 'c_user',
        'c_usage': 'c_usage'
    }

    def __init__(self, time=None, c_idle=None, c_iowait=None, c_system=None, c_user=None, c_usage=None, local_vars_configuration=None):  # noqa: E501
        """CPUStat - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._time = None
        self._c_idle = None
        self._c_iowait = None
        self._c_system = None
        self._c_user = None
        self._c_usage = None
        self.discriminator = None

        self.time = time
        self.c_idle = c_idle
        self.c_iowait = c_iowait
        self.c_system = c_system
        self.c_user = c_user
        self.c_usage = c_usage

    @property
    def time(self):
        """Gets the time of this CPUStat.  # noqa: E501


        :return: The time of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this CPUStat.


        :param time: The time of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and time is None:  # noqa: E501
            raise ValueError("Invalid value for `time`, must not be `None`")  # noqa: E501

        self._time = time

    @property
    def c_idle(self):
        """Gets the c_idle of this CPUStat.  # noqa: E501


        :return: The c_idle of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._c_idle

    @c_idle.setter
    def c_idle(self, c_idle):
        """Sets the c_idle of this CPUStat.


        :param c_idle: The c_idle of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and c_idle is None:  # noqa: E501
            raise ValueError("Invalid value for `c_idle`, must not be `None`")  # noqa: E501

        self._c_idle = c_idle

    @property
    def c_iowait(self):
        """Gets the c_iowait of this CPUStat.  # noqa: E501


        :return: The c_iowait of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._c_iowait

    @c_iowait.setter
    def c_iowait(self, c_iowait):
        """Sets the c_iowait of this CPUStat.


        :param c_iowait: The c_iowait of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and c_iowait is None:  # noqa: E501
            raise ValueError("Invalid value for `c_iowait`, must not be `None`")  # noqa: E501

        self._c_iowait = c_iowait

    @property
    def c_system(self):
        """Gets the c_system of this CPUStat.  # noqa: E501


        :return: The c_system of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._c_system

    @c_system.setter
    def c_system(self, c_system):
        """Sets the c_system of this CPUStat.


        :param c_system: The c_system of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and c_system is None:  # noqa: E501
            raise ValueError("Invalid value for `c_system`, must not be `None`")  # noqa: E501

        self._c_system = c_system

    @property
    def c_user(self):
        """Gets the c_user of this CPUStat.  # noqa: E501


        :return: The c_user of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._c_user

    @c_user.setter
    def c_user(self, c_user):
        """Sets the c_user of this CPUStat.


        :param c_user: The c_user of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and c_user is None:  # noqa: E501
            raise ValueError("Invalid value for `c_user`, must not be `None`")  # noqa: E501

        self._c_user = c_user

    @property
    def c_usage(self):
        """Gets the c_usage of this CPUStat.  # noqa: E501


        :return: The c_usage of this CPUStat.  # noqa: E501
        :rtype: float
        """
        return self._c_usage

    @c_usage.setter
    def c_usage(self, c_usage):
        """Sets the c_usage of this CPUStat.


        :param c_usage: The c_usage of this CPUStat.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and c_usage is None:  # noqa: E501
            raise ValueError("Invalid value for `c_usage`, must not be `None`")  # noqa: E501

        self._c_usage = c_usage

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
        if not isinstance(other, CPUStat):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CPUStat):
            return True

        return self.to_dict() != other.to_dict()
