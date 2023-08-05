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


class AWSAccountPartialUpdate(object):
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
        'name': 'str',
        'access_key_id': 'str',
        'secret_access_key': 'str',
        'endpoint_url': 'str',
        'default_region': 'str'
    }

    attribute_map = {
        'name': 'name',
        'access_key_id': 'access_key_id',
        'secret_access_key': 'secret_access_key',
        'endpoint_url': 'endpoint_url',
        'default_region': 'default_region'
    }

    def __init__(self, name=None, access_key_id=None, secret_access_key=None, endpoint_url=None, default_region=None, local_vars_configuration=None):  # noqa: E501
        """AWSAccountPartialUpdate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._access_key_id = None
        self._secret_access_key = None
        self._endpoint_url = None
        self._default_region = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if access_key_id is not None:
            self.access_key_id = access_key_id
        if secret_access_key is not None:
            self.secret_access_key = secret_access_key
        self.endpoint_url = endpoint_url
        if default_region is not None:
            self.default_region = default_region

    @property
    def name(self):
        """Gets the name of this AWSAccountPartialUpdate.  # noqa: E501


        :return: The name of this AWSAccountPartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AWSAccountPartialUpdate.


        :param name: The name of this AWSAccountPartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 255):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def access_key_id(self):
        """Gets the access_key_id of this AWSAccountPartialUpdate.  # noqa: E501


        :return: The access_key_id of this AWSAccountPartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._access_key_id

    @access_key_id.setter
    def access_key_id(self, access_key_id):
        """Sets the access_key_id of this AWSAccountPartialUpdate.


        :param access_key_id: The access_key_id of this AWSAccountPartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                access_key_id is not None and len(access_key_id) > 255):
            raise ValueError("Invalid value for `access_key_id`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                access_key_id is not None and len(access_key_id) < 1):
            raise ValueError("Invalid value for `access_key_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._access_key_id = access_key_id

    @property
    def secret_access_key(self):
        """Gets the secret_access_key of this AWSAccountPartialUpdate.  # noqa: E501


        :return: The secret_access_key of this AWSAccountPartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._secret_access_key

    @secret_access_key.setter
    def secret_access_key(self, secret_access_key):
        """Sets the secret_access_key of this AWSAccountPartialUpdate.


        :param secret_access_key: The secret_access_key of this AWSAccountPartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                secret_access_key is not None and len(secret_access_key) > 255):
            raise ValueError("Invalid value for `secret_access_key`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                secret_access_key is not None and len(secret_access_key) < 1):
            raise ValueError("Invalid value for `secret_access_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._secret_access_key = secret_access_key

    @property
    def endpoint_url(self):
        """Gets the endpoint_url of this AWSAccountPartialUpdate.  # noqa: E501


        :return: The endpoint_url of this AWSAccountPartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint_url):
        """Sets the endpoint_url of this AWSAccountPartialUpdate.


        :param endpoint_url: The endpoint_url of this AWSAccountPartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                endpoint_url is not None and len(endpoint_url) > 255):
            raise ValueError("Invalid value for `endpoint_url`, length must be less than or equal to `255`")  # noqa: E501

        self._endpoint_url = endpoint_url

    @property
    def default_region(self):
        """Gets the default_region of this AWSAccountPartialUpdate.  # noqa: E501


        :return: The default_region of this AWSAccountPartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._default_region

    @default_region.setter
    def default_region(self, default_region):
        """Sets the default_region of this AWSAccountPartialUpdate.


        :param default_region: The default_region of this AWSAccountPartialUpdate.  # noqa: E501
        :type: str
        """
        allowed_values = ["us-east-2", "us-east-1", "us-west-1", "us-west-2", "ap-east-1", "ap-south-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "cn-north-1", "cn-northwest-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and default_region not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `default_region` ({0}), must be one of {1}"  # noqa: E501
                .format(default_region, allowed_values)
            )

        self._default_region = default_region

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
        if not isinstance(other, AWSAccountPartialUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AWSAccountPartialUpdate):
            return True

        return self.to_dict() != other.to_dict()
