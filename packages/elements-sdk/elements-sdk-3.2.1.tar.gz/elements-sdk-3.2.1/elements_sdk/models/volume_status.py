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


class VolumeStatus(object):
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
        'online': 'bool',
        'size_total': 'int',
        'size_used': 'int',
        'size_free': 'int',
        'snfs': 'VolumeSNFSStatus',
        'lizardfs': 'VolumeLizardFSStatus',
        'beegfs': 'VolumeBeeGFSStatus'
    }

    attribute_map = {
        'online': 'online',
        'size_total': 'size_total',
        'size_used': 'size_used',
        'size_free': 'size_free',
        'snfs': 'snfs',
        'lizardfs': 'lizardfs',
        'beegfs': 'beegfs'
    }

    def __init__(self, online=None, size_total=None, size_used=None, size_free=None, snfs=None, lizardfs=None, beegfs=None, local_vars_configuration=None):  # noqa: E501
        """VolumeStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._online = None
        self._size_total = None
        self._size_used = None
        self._size_free = None
        self._snfs = None
        self._lizardfs = None
        self._beegfs = None
        self.discriminator = None

        self.online = online
        self.size_total = size_total
        self.size_used = size_used
        self.size_free = size_free
        if snfs is not None:
            self.snfs = snfs
        if lizardfs is not None:
            self.lizardfs = lizardfs
        if beegfs is not None:
            self.beegfs = beegfs

    @property
    def online(self):
        """Gets the online of this VolumeStatus.  # noqa: E501


        :return: The online of this VolumeStatus.  # noqa: E501
        :rtype: bool
        """
        return self._online

    @online.setter
    def online(self, online):
        """Sets the online of this VolumeStatus.


        :param online: The online of this VolumeStatus.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and online is None:  # noqa: E501
            raise ValueError("Invalid value for `online`, must not be `None`")  # noqa: E501

        self._online = online

    @property
    def size_total(self):
        """Gets the size_total of this VolumeStatus.  # noqa: E501


        :return: The size_total of this VolumeStatus.  # noqa: E501
        :rtype: int
        """
        return self._size_total

    @size_total.setter
    def size_total(self, size_total):
        """Sets the size_total of this VolumeStatus.


        :param size_total: The size_total of this VolumeStatus.  # noqa: E501
        :type: int
        """

        self._size_total = size_total

    @property
    def size_used(self):
        """Gets the size_used of this VolumeStatus.  # noqa: E501


        :return: The size_used of this VolumeStatus.  # noqa: E501
        :rtype: int
        """
        return self._size_used

    @size_used.setter
    def size_used(self, size_used):
        """Sets the size_used of this VolumeStatus.


        :param size_used: The size_used of this VolumeStatus.  # noqa: E501
        :type: int
        """

        self._size_used = size_used

    @property
    def size_free(self):
        """Gets the size_free of this VolumeStatus.  # noqa: E501


        :return: The size_free of this VolumeStatus.  # noqa: E501
        :rtype: int
        """
        return self._size_free

    @size_free.setter
    def size_free(self, size_free):
        """Sets the size_free of this VolumeStatus.


        :param size_free: The size_free of this VolumeStatus.  # noqa: E501
        :type: int
        """

        self._size_free = size_free

    @property
    def snfs(self):
        """Gets the snfs of this VolumeStatus.  # noqa: E501


        :return: The snfs of this VolumeStatus.  # noqa: E501
        :rtype: VolumeSNFSStatus
        """
        return self._snfs

    @snfs.setter
    def snfs(self, snfs):
        """Sets the snfs of this VolumeStatus.


        :param snfs: The snfs of this VolumeStatus.  # noqa: E501
        :type: VolumeSNFSStatus
        """

        self._snfs = snfs

    @property
    def lizardfs(self):
        """Gets the lizardfs of this VolumeStatus.  # noqa: E501


        :return: The lizardfs of this VolumeStatus.  # noqa: E501
        :rtype: VolumeLizardFSStatus
        """
        return self._lizardfs

    @lizardfs.setter
    def lizardfs(self, lizardfs):
        """Sets the lizardfs of this VolumeStatus.


        :param lizardfs: The lizardfs of this VolumeStatus.  # noqa: E501
        :type: VolumeLizardFSStatus
        """

        self._lizardfs = lizardfs

    @property
    def beegfs(self):
        """Gets the beegfs of this VolumeStatus.  # noqa: E501


        :return: The beegfs of this VolumeStatus.  # noqa: E501
        :rtype: VolumeBeeGFSStatus
        """
        return self._beegfs

    @beegfs.setter
    def beegfs(self, beegfs):
        """Sets the beegfs of this VolumeStatus.


        :param beegfs: The beegfs of this VolumeStatus.  # noqa: E501
        :type: VolumeBeeGFSStatus
        """

        self._beegfs = beegfs

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
        if not isinstance(other, VolumeStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VolumeStatus):
            return True

        return self.to_dict() != other.to_dict()
