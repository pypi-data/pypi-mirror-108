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


class UploadChunkEndpointRequest(object):
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
        'upload_id': 'str',
        'chunk_number': 'int',
        'total_chunks': 'int'
    }

    attribute_map = {
        'upload_id': 'upload_id',
        'chunk_number': 'chunk_number',
        'total_chunks': 'total_chunks'
    }

    def __init__(self, upload_id=None, chunk_number=None, total_chunks=None, local_vars_configuration=None):  # noqa: E501
        """UploadChunkEndpointRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._upload_id = None
        self._chunk_number = None
        self._total_chunks = None
        self.discriminator = None

        if upload_id is not None:
            self.upload_id = upload_id
        if chunk_number is not None:
            self.chunk_number = chunk_number
        if total_chunks is not None:
            self.total_chunks = total_chunks

    @property
    def upload_id(self):
        """Gets the upload_id of this UploadChunkEndpointRequest.  # noqa: E501


        :return: The upload_id of this UploadChunkEndpointRequest.  # noqa: E501
        :rtype: str
        """
        return self._upload_id

    @upload_id.setter
    def upload_id(self, upload_id):
        """Sets the upload_id of this UploadChunkEndpointRequest.


        :param upload_id: The upload_id of this UploadChunkEndpointRequest.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                upload_id is not None and len(upload_id) < 1):
            raise ValueError("Invalid value for `upload_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._upload_id = upload_id

    @property
    def chunk_number(self):
        """Gets the chunk_number of this UploadChunkEndpointRequest.  # noqa: E501


        :return: The chunk_number of this UploadChunkEndpointRequest.  # noqa: E501
        :rtype: int
        """
        return self._chunk_number

    @chunk_number.setter
    def chunk_number(self, chunk_number):
        """Sets the chunk_number of this UploadChunkEndpointRequest.


        :param chunk_number: The chunk_number of this UploadChunkEndpointRequest.  # noqa: E501
        :type: int
        """

        self._chunk_number = chunk_number

    @property
    def total_chunks(self):
        """Gets the total_chunks of this UploadChunkEndpointRequest.  # noqa: E501


        :return: The total_chunks of this UploadChunkEndpointRequest.  # noqa: E501
        :rtype: int
        """
        return self._total_chunks

    @total_chunks.setter
    def total_chunks(self, total_chunks):
        """Sets the total_chunks of this UploadChunkEndpointRequest.


        :param total_chunks: The total_chunks of this UploadChunkEndpointRequest.  # noqa: E501
        :type: int
        """

        self._total_chunks = total_chunks

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
        if not isinstance(other, UploadChunkEndpointRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UploadChunkEndpointRequest):
            return True

        return self.to_dict() != other.to_dict()
