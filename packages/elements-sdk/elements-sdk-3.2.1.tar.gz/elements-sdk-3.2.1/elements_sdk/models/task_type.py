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


class TaskType(object):
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
        'type': 'str',
        'display_name': 'str',
        'display_group': 'str',
        'input_type': 'str',
        'abortable': 'bool',
        'arg_template': 'dict(str, str)',
        'arg_types': 'dict(str, ArgumentType)',
        'required_args': 'list[str]',
        'output_names': 'dict(str, str)',
        'output_types': 'dict(str, ArgumentType)',
        'parameters_editor_component': 'str',
        'superuser_only': 'bool',
        'icon_class': 'str',
        'is_available': 'bool',
        'allow_in_jobs': 'bool'
    }

    attribute_map = {
        'type': 'type',
        'display_name': 'display_name',
        'display_group': 'display_group',
        'input_type': 'input_type',
        'abortable': 'abortable',
        'arg_template': 'arg_template',
        'arg_types': 'arg_types',
        'required_args': 'required_args',
        'output_names': 'output_names',
        'output_types': 'output_types',
        'parameters_editor_component': 'parameters_editor_component',
        'superuser_only': 'superuser_only',
        'icon_class': 'icon_class',
        'is_available': 'is_available',
        'allow_in_jobs': 'allow_in_jobs'
    }

    def __init__(self, type=None, display_name=None, display_group=None, input_type=None, abortable=None, arg_template=None, arg_types=None, required_args=None, output_names=None, output_types=None, parameters_editor_component=None, superuser_only=None, icon_class=None, is_available=None, allow_in_jobs=None, local_vars_configuration=None):  # noqa: E501
        """TaskType - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._display_name = None
        self._display_group = None
        self._input_type = None
        self._abortable = None
        self._arg_template = None
        self._arg_types = None
        self._required_args = None
        self._output_names = None
        self._output_types = None
        self._parameters_editor_component = None
        self._superuser_only = None
        self._icon_class = None
        self._is_available = None
        self._allow_in_jobs = None
        self.discriminator = None

        self.type = type
        self.display_name = display_name
        self.display_group = display_group
        self.input_type = input_type
        self.abortable = abortable
        self.arg_template = arg_template
        if arg_types is not None:
            self.arg_types = arg_types
        self.required_args = required_args
        self.output_names = output_names
        if output_types is not None:
            self.output_types = output_types
        self.parameters_editor_component = parameters_editor_component
        self.superuser_only = superuser_only
        self.icon_class = icon_class
        if is_available is not None:
            self.is_available = is_available
        self.allow_in_jobs = allow_in_jobs

    @property
    def type(self):
        """Gets the type of this TaskType.  # noqa: E501


        :return: The type of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TaskType.


        :param type: The type of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def display_name(self):
        """Gets the display_name of this TaskType.  # noqa: E501


        :return: The display_name of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this TaskType.


        :param display_name: The display_name of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 1):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._display_name = display_name

    @property
    def display_group(self):
        """Gets the display_group of this TaskType.  # noqa: E501


        :return: The display_group of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._display_group

    @display_group.setter
    def display_group(self, display_group):
        """Sets the display_group of this TaskType.


        :param display_group: The display_group of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and display_group is None:  # noqa: E501
            raise ValueError("Invalid value for `display_group`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_group is not None and len(display_group) < 1):
            raise ValueError("Invalid value for `display_group`, length must be greater than or equal to `1`")  # noqa: E501

        self._display_group = display_group

    @property
    def input_type(self):
        """Gets the input_type of this TaskType.  # noqa: E501


        :return: The input_type of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._input_type

    @input_type.setter
    def input_type(self, input_type):
        """Sets the input_type of this TaskType.


        :param input_type: The input_type of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and input_type is None:  # noqa: E501
            raise ValueError("Invalid value for `input_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                input_type is not None and len(input_type) < 1):
            raise ValueError("Invalid value for `input_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._input_type = input_type

    @property
    def abortable(self):
        """Gets the abortable of this TaskType.  # noqa: E501


        :return: The abortable of this TaskType.  # noqa: E501
        :rtype: bool
        """
        return self._abortable

    @abortable.setter
    def abortable(self, abortable):
        """Sets the abortable of this TaskType.


        :param abortable: The abortable of this TaskType.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and abortable is None:  # noqa: E501
            raise ValueError("Invalid value for `abortable`, must not be `None`")  # noqa: E501

        self._abortable = abortable

    @property
    def arg_template(self):
        """Gets the arg_template of this TaskType.  # noqa: E501


        :return: The arg_template of this TaskType.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._arg_template

    @arg_template.setter
    def arg_template(self, arg_template):
        """Sets the arg_template of this TaskType.


        :param arg_template: The arg_template of this TaskType.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and arg_template is None:  # noqa: E501
            raise ValueError("Invalid value for `arg_template`, must not be `None`")  # noqa: E501

        self._arg_template = arg_template

    @property
    def arg_types(self):
        """Gets the arg_types of this TaskType.  # noqa: E501


        :return: The arg_types of this TaskType.  # noqa: E501
        :rtype: dict(str, ArgumentType)
        """
        return self._arg_types

    @arg_types.setter
    def arg_types(self, arg_types):
        """Sets the arg_types of this TaskType.


        :param arg_types: The arg_types of this TaskType.  # noqa: E501
        :type: dict(str, ArgumentType)
        """

        self._arg_types = arg_types

    @property
    def required_args(self):
        """Gets the required_args of this TaskType.  # noqa: E501


        :return: The required_args of this TaskType.  # noqa: E501
        :rtype: list[str]
        """
        return self._required_args

    @required_args.setter
    def required_args(self, required_args):
        """Sets the required_args of this TaskType.


        :param required_args: The required_args of this TaskType.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and required_args is None:  # noqa: E501
            raise ValueError("Invalid value for `required_args`, must not be `None`")  # noqa: E501

        self._required_args = required_args

    @property
    def output_names(self):
        """Gets the output_names of this TaskType.  # noqa: E501


        :return: The output_names of this TaskType.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._output_names

    @output_names.setter
    def output_names(self, output_names):
        """Sets the output_names of this TaskType.


        :param output_names: The output_names of this TaskType.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and output_names is None:  # noqa: E501
            raise ValueError("Invalid value for `output_names`, must not be `None`")  # noqa: E501

        self._output_names = output_names

    @property
    def output_types(self):
        """Gets the output_types of this TaskType.  # noqa: E501


        :return: The output_types of this TaskType.  # noqa: E501
        :rtype: dict(str, ArgumentType)
        """
        return self._output_types

    @output_types.setter
    def output_types(self, output_types):
        """Sets the output_types of this TaskType.


        :param output_types: The output_types of this TaskType.  # noqa: E501
        :type: dict(str, ArgumentType)
        """

        self._output_types = output_types

    @property
    def parameters_editor_component(self):
        """Gets the parameters_editor_component of this TaskType.  # noqa: E501


        :return: The parameters_editor_component of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._parameters_editor_component

    @parameters_editor_component.setter
    def parameters_editor_component(self, parameters_editor_component):
        """Sets the parameters_editor_component of this TaskType.


        :param parameters_editor_component: The parameters_editor_component of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and parameters_editor_component is None:  # noqa: E501
            raise ValueError("Invalid value for `parameters_editor_component`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                parameters_editor_component is not None and len(parameters_editor_component) < 1):
            raise ValueError("Invalid value for `parameters_editor_component`, length must be greater than or equal to `1`")  # noqa: E501

        self._parameters_editor_component = parameters_editor_component

    @property
    def superuser_only(self):
        """Gets the superuser_only of this TaskType.  # noqa: E501


        :return: The superuser_only of this TaskType.  # noqa: E501
        :rtype: bool
        """
        return self._superuser_only

    @superuser_only.setter
    def superuser_only(self, superuser_only):
        """Sets the superuser_only of this TaskType.


        :param superuser_only: The superuser_only of this TaskType.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and superuser_only is None:  # noqa: E501
            raise ValueError("Invalid value for `superuser_only`, must not be `None`")  # noqa: E501

        self._superuser_only = superuser_only

    @property
    def icon_class(self):
        """Gets the icon_class of this TaskType.  # noqa: E501


        :return: The icon_class of this TaskType.  # noqa: E501
        :rtype: str
        """
        return self._icon_class

    @icon_class.setter
    def icon_class(self, icon_class):
        """Sets the icon_class of this TaskType.


        :param icon_class: The icon_class of this TaskType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and icon_class is None:  # noqa: E501
            raise ValueError("Invalid value for `icon_class`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                icon_class is not None and len(icon_class) < 1):
            raise ValueError("Invalid value for `icon_class`, length must be greater than or equal to `1`")  # noqa: E501

        self._icon_class = icon_class

    @property
    def is_available(self):
        """Gets the is_available of this TaskType.  # noqa: E501


        :return: The is_available of this TaskType.  # noqa: E501
        :rtype: bool
        """
        return self._is_available

    @is_available.setter
    def is_available(self, is_available):
        """Sets the is_available of this TaskType.


        :param is_available: The is_available of this TaskType.  # noqa: E501
        :type: bool
        """

        self._is_available = is_available

    @property
    def allow_in_jobs(self):
        """Gets the allow_in_jobs of this TaskType.  # noqa: E501


        :return: The allow_in_jobs of this TaskType.  # noqa: E501
        :rtype: bool
        """
        return self._allow_in_jobs

    @allow_in_jobs.setter
    def allow_in_jobs(self, allow_in_jobs):
        """Sets the allow_in_jobs of this TaskType.


        :param allow_in_jobs: The allow_in_jobs of this TaskType.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and allow_in_jobs is None:  # noqa: E501
            raise ValueError("Invalid value for `allow_in_jobs`, must not be `None`")  # noqa: E501

        self._allow_in_jobs = allow_in_jobs

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
        if not isinstance(other, TaskType):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskType):
            return True

        return self.to_dict() != other.to_dict()
