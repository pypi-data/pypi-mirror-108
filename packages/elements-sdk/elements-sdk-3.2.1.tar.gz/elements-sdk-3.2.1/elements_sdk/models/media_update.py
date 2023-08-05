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


class MediaUpdate(object):
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
        'asset': 'AssetMini',
        'comment': 'Comment',
        'directory': 'MediaFile',
        'root': 'MediaRootMini',
        'user': 'ElementsUserMini',
        'custom_fields_diff': 'dict(str, str)',
        'added_tags': 'list[Tag]',
        'removed_tags': 'list[Tag]',
        'type': 'str',
        'date': 'datetime',
        'rating': 'int'
    }

    attribute_map = {
        'id': 'id',
        'asset': 'asset',
        'comment': 'comment',
        'directory': 'directory',
        'root': 'root',
        'user': 'user',
        'custom_fields_diff': 'custom_fields_diff',
        'added_tags': 'added_tags',
        'removed_tags': 'removed_tags',
        'type': 'type',
        'date': 'date',
        'rating': 'rating'
    }

    def __init__(self, id=None, asset=None, comment=None, directory=None, root=None, user=None, custom_fields_diff=None, added_tags=None, removed_tags=None, type=None, date=None, rating=None, local_vars_configuration=None):  # noqa: E501
        """MediaUpdate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._asset = None
        self._comment = None
        self._directory = None
        self._root = None
        self._user = None
        self._custom_fields_diff = None
        self._added_tags = None
        self._removed_tags = None
        self._type = None
        self._date = None
        self._rating = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if asset is not None:
            self.asset = asset
        if comment is not None:
            self.comment = comment
        if directory is not None:
            self.directory = directory
        if root is not None:
            self.root = root
        if user is not None:
            self.user = user
        self.custom_fields_diff = custom_fields_diff
        if added_tags is not None:
            self.added_tags = added_tags
        if removed_tags is not None:
            self.removed_tags = removed_tags
        self.type = type
        if date is not None:
            self.date = date
        self.rating = rating

    @property
    def id(self):
        """Gets the id of this MediaUpdate.  # noqa: E501


        :return: The id of this MediaUpdate.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MediaUpdate.


        :param id: The id of this MediaUpdate.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def asset(self):
        """Gets the asset of this MediaUpdate.  # noqa: E501


        :return: The asset of this MediaUpdate.  # noqa: E501
        :rtype: AssetMini
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this MediaUpdate.


        :param asset: The asset of this MediaUpdate.  # noqa: E501
        :type: AssetMini
        """

        self._asset = asset

    @property
    def comment(self):
        """Gets the comment of this MediaUpdate.  # noqa: E501


        :return: The comment of this MediaUpdate.  # noqa: E501
        :rtype: Comment
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this MediaUpdate.


        :param comment: The comment of this MediaUpdate.  # noqa: E501
        :type: Comment
        """

        self._comment = comment

    @property
    def directory(self):
        """Gets the directory of this MediaUpdate.  # noqa: E501


        :return: The directory of this MediaUpdate.  # noqa: E501
        :rtype: MediaFile
        """
        return self._directory

    @directory.setter
    def directory(self, directory):
        """Sets the directory of this MediaUpdate.


        :param directory: The directory of this MediaUpdate.  # noqa: E501
        :type: MediaFile
        """

        self._directory = directory

    @property
    def root(self):
        """Gets the root of this MediaUpdate.  # noqa: E501


        :return: The root of this MediaUpdate.  # noqa: E501
        :rtype: MediaRootMini
        """
        return self._root

    @root.setter
    def root(self, root):
        """Sets the root of this MediaUpdate.


        :param root: The root of this MediaUpdate.  # noqa: E501
        :type: MediaRootMini
        """

        self._root = root

    @property
    def user(self):
        """Gets the user of this MediaUpdate.  # noqa: E501


        :return: The user of this MediaUpdate.  # noqa: E501
        :rtype: ElementsUserMini
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this MediaUpdate.


        :param user: The user of this MediaUpdate.  # noqa: E501
        :type: ElementsUserMini
        """

        self._user = user

    @property
    def custom_fields_diff(self):
        """Gets the custom_fields_diff of this MediaUpdate.  # noqa: E501


        :return: The custom_fields_diff of this MediaUpdate.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._custom_fields_diff

    @custom_fields_diff.setter
    def custom_fields_diff(self, custom_fields_diff):
        """Sets the custom_fields_diff of this MediaUpdate.


        :param custom_fields_diff: The custom_fields_diff of this MediaUpdate.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and custom_fields_diff is None:  # noqa: E501
            raise ValueError("Invalid value for `custom_fields_diff`, must not be `None`")  # noqa: E501

        self._custom_fields_diff = custom_fields_diff

    @property
    def added_tags(self):
        """Gets the added_tags of this MediaUpdate.  # noqa: E501


        :return: The added_tags of this MediaUpdate.  # noqa: E501
        :rtype: list[Tag]
        """
        return self._added_tags

    @added_tags.setter
    def added_tags(self, added_tags):
        """Sets the added_tags of this MediaUpdate.


        :param added_tags: The added_tags of this MediaUpdate.  # noqa: E501
        :type: list[Tag]
        """

        self._added_tags = added_tags

    @property
    def removed_tags(self):
        """Gets the removed_tags of this MediaUpdate.  # noqa: E501


        :return: The removed_tags of this MediaUpdate.  # noqa: E501
        :rtype: list[Tag]
        """
        return self._removed_tags

    @removed_tags.setter
    def removed_tags(self, removed_tags):
        """Sets the removed_tags of this MediaUpdate.


        :param removed_tags: The removed_tags of this MediaUpdate.  # noqa: E501
        :type: list[Tag]
        """

        self._removed_tags = removed_tags

    @property
    def type(self):
        """Gets the type of this MediaUpdate.  # noqa: E501


        :return: The type of this MediaUpdate.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MediaUpdate.


        :param type: The type of this MediaUpdate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) > 63):
            raise ValueError("Invalid value for `type`, length must be less than or equal to `63`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def date(self):
        """Gets the date of this MediaUpdate.  # noqa: E501


        :return: The date of this MediaUpdate.  # noqa: E501
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this MediaUpdate.


        :param date: The date of this MediaUpdate.  # noqa: E501
        :type: datetime
        """

        self._date = date

    @property
    def rating(self):
        """Gets the rating of this MediaUpdate.  # noqa: E501


        :return: The rating of this MediaUpdate.  # noqa: E501
        :rtype: int
        """
        return self._rating

    @rating.setter
    def rating(self, rating):
        """Sets the rating of this MediaUpdate.


        :param rating: The rating of this MediaUpdate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                rating is not None and rating > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `rating`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                rating is not None and rating < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `rating`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._rating = rating

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
        if not isinstance(other, MediaUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MediaUpdate):
            return True

        return self.to_dict() != other.to_dict()
