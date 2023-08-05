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


class MediaFile(object):
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
        'volume': 'VolumeMini',
        'info': 'object',
        'custom_fields': 'object',
        'resolved_permission': 'MediaRootPermission',
        'parent': 'dict(str, str)',
        'root': 'MediaRootMini',
        'effective_custom_fields': 'dict(str, str)',
        'modified_by': 'ElementsUserMini',
        'full_path': 'str',
        'search_highlight': 'str',
        'is_shared': 'bool',
        'name': 'str',
        'path': 'str',
        'pathhash': 'str',
        'is_dir': 'bool',
        'total_files': 'int',
        'size': 'int',
        'mtime': 'int',
        'present': 'bool',
        'needs_rescan': 'bool',
        'is_showroom': 'bool',
        'bundle_index': 'int',
        'modified': 'datetime',
        'bundle': 'int'
    }

    attribute_map = {
        'id': 'id',
        'volume': 'volume',
        'info': 'info',
        'custom_fields': 'custom_fields',
        'resolved_permission': 'resolved_permission',
        'parent': 'parent',
        'root': 'root',
        'effective_custom_fields': 'effective_custom_fields',
        'modified_by': 'modified_by',
        'full_path': 'full_path',
        'search_highlight': 'search_highlight',
        'is_shared': 'is_shared',
        'name': 'name',
        'path': 'path',
        'pathhash': 'pathhash',
        'is_dir': 'is_dir',
        'total_files': 'total_files',
        'size': 'size',
        'mtime': 'mtime',
        'present': 'present',
        'needs_rescan': 'needs_rescan',
        'is_showroom': 'is_showroom',
        'bundle_index': 'bundle_index',
        'modified': 'modified',
        'bundle': 'bundle'
    }

    def __init__(self, id=None, volume=None, info=None, custom_fields=None, resolved_permission=None, parent=None, root=None, effective_custom_fields=None, modified_by=None, full_path=None, search_highlight=None, is_shared=None, name=None, path=None, pathhash=None, is_dir=None, total_files=None, size=None, mtime=None, present=None, needs_rescan=None, is_showroom=None, bundle_index=None, modified=None, bundle=None, local_vars_configuration=None):  # noqa: E501
        """MediaFile - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._volume = None
        self._info = None
        self._custom_fields = None
        self._resolved_permission = None
        self._parent = None
        self._root = None
        self._effective_custom_fields = None
        self._modified_by = None
        self._full_path = None
        self._search_highlight = None
        self._is_shared = None
        self._name = None
        self._path = None
        self._pathhash = None
        self._is_dir = None
        self._total_files = None
        self._size = None
        self._mtime = None
        self._present = None
        self._needs_rescan = None
        self._is_showroom = None
        self._bundle_index = None
        self._modified = None
        self._bundle = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if volume is not None:
            self.volume = volume
        if info is not None:
            self.info = info
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if resolved_permission is not None:
            self.resolved_permission = resolved_permission
        if parent is not None:
            self.parent = parent
        if root is not None:
            self.root = root
        if effective_custom_fields is not None:
            self.effective_custom_fields = effective_custom_fields
        if modified_by is not None:
            self.modified_by = modified_by
        if full_path is not None:
            self.full_path = full_path
        if search_highlight is not None:
            self.search_highlight = search_highlight
        if is_shared is not None:
            self.is_shared = is_shared
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if pathhash is not None:
            self.pathhash = pathhash
        if is_dir is not None:
            self.is_dir = is_dir
        self.total_files = total_files
        if size is not None:
            self.size = size
        if mtime is not None:
            self.mtime = mtime
        if present is not None:
            self.present = present
        if needs_rescan is not None:
            self.needs_rescan = needs_rescan
        if is_showroom is not None:
            self.is_showroom = is_showroom
        if bundle_index is not None:
            self.bundle_index = bundle_index
        if modified is not None:
            self.modified = modified
        if bundle is not None:
            self.bundle = bundle

    @property
    def id(self):
        """Gets the id of this MediaFile.  # noqa: E501


        :return: The id of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MediaFile.


        :param id: The id of this MediaFile.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def volume(self):
        """Gets the volume of this MediaFile.  # noqa: E501


        :return: The volume of this MediaFile.  # noqa: E501
        :rtype: VolumeMini
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this MediaFile.


        :param volume: The volume of this MediaFile.  # noqa: E501
        :type: VolumeMini
        """

        self._volume = volume

    @property
    def info(self):
        """Gets the info of this MediaFile.  # noqa: E501


        :return: The info of this MediaFile.  # noqa: E501
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this MediaFile.


        :param info: The info of this MediaFile.  # noqa: E501
        :type: object
        """

        self._info = info

    @property
    def custom_fields(self):
        """Gets the custom_fields of this MediaFile.  # noqa: E501


        :return: The custom_fields of this MediaFile.  # noqa: E501
        :rtype: object
        """
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, custom_fields):
        """Sets the custom_fields of this MediaFile.


        :param custom_fields: The custom_fields of this MediaFile.  # noqa: E501
        :type: object
        """

        self._custom_fields = custom_fields

    @property
    def resolved_permission(self):
        """Gets the resolved_permission of this MediaFile.  # noqa: E501


        :return: The resolved_permission of this MediaFile.  # noqa: E501
        :rtype: MediaRootPermission
        """
        return self._resolved_permission

    @resolved_permission.setter
    def resolved_permission(self, resolved_permission):
        """Sets the resolved_permission of this MediaFile.


        :param resolved_permission: The resolved_permission of this MediaFile.  # noqa: E501
        :type: MediaRootPermission
        """

        self._resolved_permission = resolved_permission

    @property
    def parent(self):
        """Gets the parent of this MediaFile.  # noqa: E501


        :return: The parent of this MediaFile.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this MediaFile.


        :param parent: The parent of this MediaFile.  # noqa: E501
        :type: dict(str, str)
        """

        self._parent = parent

    @property
    def root(self):
        """Gets the root of this MediaFile.  # noqa: E501


        :return: The root of this MediaFile.  # noqa: E501
        :rtype: MediaRootMini
        """
        return self._root

    @root.setter
    def root(self, root):
        """Sets the root of this MediaFile.


        :param root: The root of this MediaFile.  # noqa: E501
        :type: MediaRootMini
        """

        self._root = root

    @property
    def effective_custom_fields(self):
        """Gets the effective_custom_fields of this MediaFile.  # noqa: E501


        :return: The effective_custom_fields of this MediaFile.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._effective_custom_fields

    @effective_custom_fields.setter
    def effective_custom_fields(self, effective_custom_fields):
        """Sets the effective_custom_fields of this MediaFile.


        :param effective_custom_fields: The effective_custom_fields of this MediaFile.  # noqa: E501
        :type: dict(str, str)
        """

        self._effective_custom_fields = effective_custom_fields

    @property
    def modified_by(self):
        """Gets the modified_by of this MediaFile.  # noqa: E501


        :return: The modified_by of this MediaFile.  # noqa: E501
        :rtype: ElementsUserMini
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """Sets the modified_by of this MediaFile.


        :param modified_by: The modified_by of this MediaFile.  # noqa: E501
        :type: ElementsUserMini
        """

        self._modified_by = modified_by

    @property
    def full_path(self):
        """Gets the full_path of this MediaFile.  # noqa: E501


        :return: The full_path of this MediaFile.  # noqa: E501
        :rtype: str
        """
        return self._full_path

    @full_path.setter
    def full_path(self, full_path):
        """Sets the full_path of this MediaFile.


        :param full_path: The full_path of this MediaFile.  # noqa: E501
        :type: str
        """

        self._full_path = full_path

    @property
    def search_highlight(self):
        """Gets the search_highlight of this MediaFile.  # noqa: E501


        :return: The search_highlight of this MediaFile.  # noqa: E501
        :rtype: str
        """
        return self._search_highlight

    @search_highlight.setter
    def search_highlight(self, search_highlight):
        """Sets the search_highlight of this MediaFile.


        :param search_highlight: The search_highlight of this MediaFile.  # noqa: E501
        :type: str
        """

        self._search_highlight = search_highlight

    @property
    def is_shared(self):
        """Gets the is_shared of this MediaFile.  # noqa: E501


        :return: The is_shared of this MediaFile.  # noqa: E501
        :rtype: bool
        """
        return self._is_shared

    @is_shared.setter
    def is_shared(self, is_shared):
        """Sets the is_shared of this MediaFile.


        :param is_shared: The is_shared of this MediaFile.  # noqa: E501
        :type: bool
        """

        self._is_shared = is_shared

    @property
    def name(self):
        """Gets the name of this MediaFile.  # noqa: E501


        :return: The name of this MediaFile.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MediaFile.


        :param name: The name of this MediaFile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def path(self):
        """Gets the path of this MediaFile.  # noqa: E501


        :return: The path of this MediaFile.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this MediaFile.


        :param path: The path of this MediaFile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) < 1):
            raise ValueError("Invalid value for `path`, length must be greater than or equal to `1`")  # noqa: E501

        self._path = path

    @property
    def pathhash(self):
        """Gets the pathhash of this MediaFile.  # noqa: E501


        :return: The pathhash of this MediaFile.  # noqa: E501
        :rtype: str
        """
        return self._pathhash

    @pathhash.setter
    def pathhash(self, pathhash):
        """Sets the pathhash of this MediaFile.


        :param pathhash: The pathhash of this MediaFile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                pathhash is not None and len(pathhash) < 1):
            raise ValueError("Invalid value for `pathhash`, length must be greater than or equal to `1`")  # noqa: E501

        self._pathhash = pathhash

    @property
    def is_dir(self):
        """Gets the is_dir of this MediaFile.  # noqa: E501


        :return: The is_dir of this MediaFile.  # noqa: E501
        :rtype: bool
        """
        return self._is_dir

    @is_dir.setter
    def is_dir(self, is_dir):
        """Sets the is_dir of this MediaFile.


        :param is_dir: The is_dir of this MediaFile.  # noqa: E501
        :type: bool
        """

        self._is_dir = is_dir

    @property
    def total_files(self):
        """Gets the total_files of this MediaFile.  # noqa: E501


        :return: The total_files of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._total_files

    @total_files.setter
    def total_files(self, total_files):
        """Sets the total_files of this MediaFile.


        :param total_files: The total_files of this MediaFile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                total_files is not None and total_files > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `total_files`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                total_files is not None and total_files < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `total_files`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._total_files = total_files

    @property
    def size(self):
        """Gets the size of this MediaFile.  # noqa: E501


        :return: The size of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this MediaFile.


        :param size: The size of this MediaFile.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def mtime(self):
        """Gets the mtime of this MediaFile.  # noqa: E501


        :return: The mtime of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._mtime

    @mtime.setter
    def mtime(self, mtime):
        """Sets the mtime of this MediaFile.


        :param mtime: The mtime of this MediaFile.  # noqa: E501
        :type: int
        """

        self._mtime = mtime

    @property
    def present(self):
        """Gets the present of this MediaFile.  # noqa: E501


        :return: The present of this MediaFile.  # noqa: E501
        :rtype: bool
        """
        return self._present

    @present.setter
    def present(self, present):
        """Sets the present of this MediaFile.


        :param present: The present of this MediaFile.  # noqa: E501
        :type: bool
        """

        self._present = present

    @property
    def needs_rescan(self):
        """Gets the needs_rescan of this MediaFile.  # noqa: E501


        :return: The needs_rescan of this MediaFile.  # noqa: E501
        :rtype: bool
        """
        return self._needs_rescan

    @needs_rescan.setter
    def needs_rescan(self, needs_rescan):
        """Sets the needs_rescan of this MediaFile.


        :param needs_rescan: The needs_rescan of this MediaFile.  # noqa: E501
        :type: bool
        """

        self._needs_rescan = needs_rescan

    @property
    def is_showroom(self):
        """Gets the is_showroom of this MediaFile.  # noqa: E501


        :return: The is_showroom of this MediaFile.  # noqa: E501
        :rtype: bool
        """
        return self._is_showroom

    @is_showroom.setter
    def is_showroom(self, is_showroom):
        """Sets the is_showroom of this MediaFile.


        :param is_showroom: The is_showroom of this MediaFile.  # noqa: E501
        :type: bool
        """

        self._is_showroom = is_showroom

    @property
    def bundle_index(self):
        """Gets the bundle_index of this MediaFile.  # noqa: E501


        :return: The bundle_index of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._bundle_index

    @bundle_index.setter
    def bundle_index(self, bundle_index):
        """Sets the bundle_index of this MediaFile.


        :param bundle_index: The bundle_index of this MediaFile.  # noqa: E501
        :type: int
        """

        self._bundle_index = bundle_index

    @property
    def modified(self):
        """Gets the modified of this MediaFile.  # noqa: E501


        :return: The modified of this MediaFile.  # noqa: E501
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this MediaFile.


        :param modified: The modified of this MediaFile.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def bundle(self):
        """Gets the bundle of this MediaFile.  # noqa: E501


        :return: The bundle of this MediaFile.  # noqa: E501
        :rtype: int
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """Sets the bundle of this MediaFile.


        :param bundle: The bundle of this MediaFile.  # noqa: E501
        :type: int
        """

        self._bundle = bundle

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
        if not isinstance(other, MediaFile):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MediaFile):
            return True

        return self.to_dict() != other.to_dict()
