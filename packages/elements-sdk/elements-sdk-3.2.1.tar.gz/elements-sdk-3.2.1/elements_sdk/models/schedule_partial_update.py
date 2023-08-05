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


class SchedulePartialUpdate(object):
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
        'variables': 'dict(str, str)',
        'type': 'int',
        'enabled': 'bool',
        'last_run': 'datetime',
        'every': 'int',
        'period': 'str',
        'crontab_day_of_month': 'str',
        'crontab_day_of_week': 'str',
        'crontab_hour': 'str',
        'crontab_minute': 'str',
        'crontab_month_of_year': 'str',
        'job': 'int'
    }

    attribute_map = {
        'variables': 'variables',
        'type': 'type',
        'enabled': 'enabled',
        'last_run': 'last_run',
        'every': 'every',
        'period': 'period',
        'crontab_day_of_month': 'crontab_day_of_month',
        'crontab_day_of_week': 'crontab_day_of_week',
        'crontab_hour': 'crontab_hour',
        'crontab_minute': 'crontab_minute',
        'crontab_month_of_year': 'crontab_month_of_year',
        'job': 'job'
    }

    def __init__(self, variables=None, type=None, enabled=None, last_run=None, every=None, period=None, crontab_day_of_month=None, crontab_day_of_week=None, crontab_hour=None, crontab_minute=None, crontab_month_of_year=None, job=None, local_vars_configuration=None):  # noqa: E501
        """SchedulePartialUpdate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._variables = None
        self._type = None
        self._enabled = None
        self._last_run = None
        self._every = None
        self._period = None
        self._crontab_day_of_month = None
        self._crontab_day_of_week = None
        self._crontab_hour = None
        self._crontab_minute = None
        self._crontab_month_of_year = None
        self._job = None
        self.discriminator = None

        if variables is not None:
            self.variables = variables
        if type is not None:
            self.type = type
        if enabled is not None:
            self.enabled = enabled
        self.last_run = last_run
        if every is not None:
            self.every = every
        if period is not None:
            self.period = period
        if crontab_day_of_month is not None:
            self.crontab_day_of_month = crontab_day_of_month
        if crontab_day_of_week is not None:
            self.crontab_day_of_week = crontab_day_of_week
        if crontab_hour is not None:
            self.crontab_hour = crontab_hour
        if crontab_minute is not None:
            self.crontab_minute = crontab_minute
        if crontab_month_of_year is not None:
            self.crontab_month_of_year = crontab_month_of_year
        if job is not None:
            self.job = job

    @property
    def variables(self):
        """Gets the variables of this SchedulePartialUpdate.  # noqa: E501


        :return: The variables of this SchedulePartialUpdate.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """Sets the variables of this SchedulePartialUpdate.


        :param variables: The variables of this SchedulePartialUpdate.  # noqa: E501
        :type: dict(str, str)
        """

        self._variables = variables

    @property
    def type(self):
        """Gets the type of this SchedulePartialUpdate.  # noqa: E501


        :return: The type of this SchedulePartialUpdate.  # noqa: E501
        :rtype: int
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SchedulePartialUpdate.


        :param type: The type of this SchedulePartialUpdate.  # noqa: E501
        :type: int
        """

        self._type = type

    @property
    def enabled(self):
        """Gets the enabled of this SchedulePartialUpdate.  # noqa: E501


        :return: The enabled of this SchedulePartialUpdate.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this SchedulePartialUpdate.


        :param enabled: The enabled of this SchedulePartialUpdate.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def last_run(self):
        """Gets the last_run of this SchedulePartialUpdate.  # noqa: E501


        :return: The last_run of this SchedulePartialUpdate.  # noqa: E501
        :rtype: datetime
        """
        return self._last_run

    @last_run.setter
    def last_run(self, last_run):
        """Sets the last_run of this SchedulePartialUpdate.


        :param last_run: The last_run of this SchedulePartialUpdate.  # noqa: E501
        :type: datetime
        """

        self._last_run = last_run

    @property
    def every(self):
        """Gets the every of this SchedulePartialUpdate.  # noqa: E501


        :return: The every of this SchedulePartialUpdate.  # noqa: E501
        :rtype: int
        """
        return self._every

    @every.setter
    def every(self, every):
        """Sets the every of this SchedulePartialUpdate.


        :param every: The every of this SchedulePartialUpdate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                every is not None and every > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `every`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                every is not None and every < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `every`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._every = every

    @property
    def period(self):
        """Gets the period of this SchedulePartialUpdate.  # noqa: E501


        :return: The period of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this SchedulePartialUpdate.


        :param period: The period of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        allowed_values = ["minutes", "hours", "days"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and period not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `period` ({0}), must be one of {1}"  # noqa: E501
                .format(period, allowed_values)
            )

        self._period = period

    @property
    def crontab_day_of_month(self):
        """Gets the crontab_day_of_month of this SchedulePartialUpdate.  # noqa: E501


        :return: The crontab_day_of_month of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._crontab_day_of_month

    @crontab_day_of_month.setter
    def crontab_day_of_month(self, crontab_day_of_month):
        """Sets the crontab_day_of_month of this SchedulePartialUpdate.


        :param crontab_day_of_month: The crontab_day_of_month of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                crontab_day_of_month is not None and len(crontab_day_of_month) > 31):
            raise ValueError("Invalid value for `crontab_day_of_month`, length must be less than or equal to `31`")  # noqa: E501

        self._crontab_day_of_month = crontab_day_of_month

    @property
    def crontab_day_of_week(self):
        """Gets the crontab_day_of_week of this SchedulePartialUpdate.  # noqa: E501


        :return: The crontab_day_of_week of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._crontab_day_of_week

    @crontab_day_of_week.setter
    def crontab_day_of_week(self, crontab_day_of_week):
        """Sets the crontab_day_of_week of this SchedulePartialUpdate.


        :param crontab_day_of_week: The crontab_day_of_week of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                crontab_day_of_week is not None and len(crontab_day_of_week) > 31):
            raise ValueError("Invalid value for `crontab_day_of_week`, length must be less than or equal to `31`")  # noqa: E501

        self._crontab_day_of_week = crontab_day_of_week

    @property
    def crontab_hour(self):
        """Gets the crontab_hour of this SchedulePartialUpdate.  # noqa: E501


        :return: The crontab_hour of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._crontab_hour

    @crontab_hour.setter
    def crontab_hour(self, crontab_hour):
        """Sets the crontab_hour of this SchedulePartialUpdate.


        :param crontab_hour: The crontab_hour of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                crontab_hour is not None and len(crontab_hour) > 31):
            raise ValueError("Invalid value for `crontab_hour`, length must be less than or equal to `31`")  # noqa: E501

        self._crontab_hour = crontab_hour

    @property
    def crontab_minute(self):
        """Gets the crontab_minute of this SchedulePartialUpdate.  # noqa: E501


        :return: The crontab_minute of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._crontab_minute

    @crontab_minute.setter
    def crontab_minute(self, crontab_minute):
        """Sets the crontab_minute of this SchedulePartialUpdate.


        :param crontab_minute: The crontab_minute of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                crontab_minute is not None and len(crontab_minute) > 31):
            raise ValueError("Invalid value for `crontab_minute`, length must be less than or equal to `31`")  # noqa: E501

        self._crontab_minute = crontab_minute

    @property
    def crontab_month_of_year(self):
        """Gets the crontab_month_of_year of this SchedulePartialUpdate.  # noqa: E501


        :return: The crontab_month_of_year of this SchedulePartialUpdate.  # noqa: E501
        :rtype: str
        """
        return self._crontab_month_of_year

    @crontab_month_of_year.setter
    def crontab_month_of_year(self, crontab_month_of_year):
        """Sets the crontab_month_of_year of this SchedulePartialUpdate.


        :param crontab_month_of_year: The crontab_month_of_year of this SchedulePartialUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                crontab_month_of_year is not None and len(crontab_month_of_year) > 31):
            raise ValueError("Invalid value for `crontab_month_of_year`, length must be less than or equal to `31`")  # noqa: E501

        self._crontab_month_of_year = crontab_month_of_year

    @property
    def job(self):
        """Gets the job of this SchedulePartialUpdate.  # noqa: E501


        :return: The job of this SchedulePartialUpdate.  # noqa: E501
        :rtype: int
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this SchedulePartialUpdate.


        :param job: The job of this SchedulePartialUpdate.  # noqa: E501
        :type: int
        """

        self._job = job

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
        if not isinstance(other, SchedulePartialUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SchedulePartialUpdate):
            return True

        return self.to_dict() != other.to_dict()
