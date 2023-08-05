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


class ProxyProfile(object):
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
        'proxy_generator': 'str',
        'resolution': 'str',
        'rate_control': 'int',
        'crf': 'int',
        'bitrate': 'int',
        'audio_bitrate': 'int',
        'variants_limit': 'int',
        'enable_realtime_read': 'bool',
        'enable_dense_filmstrip': 'bool',
        'enable_watermark': 'bool',
        'watermark_image': 'str',
        'watermark_position': 'int',
        'watermark_opacity': 'float',
        'watermark_size': 'float',
        'enable_timecode': 'bool',
        'timecode_position': 'int',
        'timecode_opacity': 'float',
        'timecode_size': 'float',
        'lut': 'str',
        'hotfolder_copy_to': 'str',
        'hotfolder_read_from': 'str',
        'hotfolder_queue_timeout': 'int',
        'hotfolder_encode_timeout': 'int',
        'vantage_workflow_id': 'str',
        'external_transcoder_staging_path': 'str',
        'external_transcoder': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'proxy_generator': 'proxy_generator',
        'resolution': 'resolution',
        'rate_control': 'rate_control',
        'crf': 'crf',
        'bitrate': 'bitrate',
        'audio_bitrate': 'audio_bitrate',
        'variants_limit': 'variants_limit',
        'enable_realtime_read': 'enable_realtime_read',
        'enable_dense_filmstrip': 'enable_dense_filmstrip',
        'enable_watermark': 'enable_watermark',
        'watermark_image': 'watermark_image',
        'watermark_position': 'watermark_position',
        'watermark_opacity': 'watermark_opacity',
        'watermark_size': 'watermark_size',
        'enable_timecode': 'enable_timecode',
        'timecode_position': 'timecode_position',
        'timecode_opacity': 'timecode_opacity',
        'timecode_size': 'timecode_size',
        'lut': 'lut',
        'hotfolder_copy_to': 'hotfolder_copy_to',
        'hotfolder_read_from': 'hotfolder_read_from',
        'hotfolder_queue_timeout': 'hotfolder_queue_timeout',
        'hotfolder_encode_timeout': 'hotfolder_encode_timeout',
        'vantage_workflow_id': 'vantage_workflow_id',
        'external_transcoder_staging_path': 'external_transcoder_staging_path',
        'external_transcoder': 'external_transcoder'
    }

    def __init__(self, id=None, name=None, proxy_generator=None, resolution=None, rate_control=None, crf=None, bitrate=None, audio_bitrate=None, variants_limit=None, enable_realtime_read=None, enable_dense_filmstrip=None, enable_watermark=None, watermark_image=None, watermark_position=None, watermark_opacity=None, watermark_size=None, enable_timecode=None, timecode_position=None, timecode_opacity=None, timecode_size=None, lut=None, hotfolder_copy_to=None, hotfolder_read_from=None, hotfolder_queue_timeout=None, hotfolder_encode_timeout=None, vantage_workflow_id=None, external_transcoder_staging_path=None, external_transcoder=None, local_vars_configuration=None):  # noqa: E501
        """ProxyProfile - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._proxy_generator = None
        self._resolution = None
        self._rate_control = None
        self._crf = None
        self._bitrate = None
        self._audio_bitrate = None
        self._variants_limit = None
        self._enable_realtime_read = None
        self._enable_dense_filmstrip = None
        self._enable_watermark = None
        self._watermark_image = None
        self._watermark_position = None
        self._watermark_opacity = None
        self._watermark_size = None
        self._enable_timecode = None
        self._timecode_position = None
        self._timecode_opacity = None
        self._timecode_size = None
        self._lut = None
        self._hotfolder_copy_to = None
        self._hotfolder_read_from = None
        self._hotfolder_queue_timeout = None
        self._hotfolder_encode_timeout = None
        self._vantage_workflow_id = None
        self._external_transcoder_staging_path = None
        self._external_transcoder = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        if proxy_generator is not None:
            self.proxy_generator = proxy_generator
        self.resolution = resolution
        if rate_control is not None:
            self.rate_control = rate_control
        self.crf = crf
        self.bitrate = bitrate
        if audio_bitrate is not None:
            self.audio_bitrate = audio_bitrate
        if variants_limit is not None:
            self.variants_limit = variants_limit
        if enable_realtime_read is not None:
            self.enable_realtime_read = enable_realtime_read
        if enable_dense_filmstrip is not None:
            self.enable_dense_filmstrip = enable_dense_filmstrip
        if enable_watermark is not None:
            self.enable_watermark = enable_watermark
        self.watermark_image = watermark_image
        if watermark_position is not None:
            self.watermark_position = watermark_position
        if watermark_opacity is not None:
            self.watermark_opacity = watermark_opacity
        if watermark_size is not None:
            self.watermark_size = watermark_size
        if enable_timecode is not None:
            self.enable_timecode = enable_timecode
        if timecode_position is not None:
            self.timecode_position = timecode_position
        if timecode_opacity is not None:
            self.timecode_opacity = timecode_opacity
        if timecode_size is not None:
            self.timecode_size = timecode_size
        self.lut = lut
        self.hotfolder_copy_to = hotfolder_copy_to
        self.hotfolder_read_from = hotfolder_read_from
        if hotfolder_queue_timeout is not None:
            self.hotfolder_queue_timeout = hotfolder_queue_timeout
        if hotfolder_encode_timeout is not None:
            self.hotfolder_encode_timeout = hotfolder_encode_timeout
        self.vantage_workflow_id = vantage_workflow_id
        self.external_transcoder_staging_path = external_transcoder_staging_path
        self.external_transcoder = external_transcoder

    @property
    def id(self):
        """Gets the id of this ProxyProfile.  # noqa: E501


        :return: The id of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProxyProfile.


        :param id: The id of this ProxyProfile.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ProxyProfile.  # noqa: E501


        :return: The name of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProxyProfile.


        :param name: The name of this ProxyProfile.  # noqa: E501
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
    def proxy_generator(self):
        """Gets the proxy_generator of this ProxyProfile.  # noqa: E501


        :return: The proxy_generator of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._proxy_generator

    @proxy_generator.setter
    def proxy_generator(self, proxy_generator):
        """Sets the proxy_generator of this ProxyProfile.


        :param proxy_generator: The proxy_generator of this ProxyProfile.  # noqa: E501
        :type: str
        """
        allowed_values = ["ffmpeg", "hotfolder", "transkoder", "vantage"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and proxy_generator not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `proxy_generator` ({0}), must be one of {1}"  # noqa: E501
                .format(proxy_generator, allowed_values)
            )

        self._proxy_generator = proxy_generator

    @property
    def resolution(self):
        """Gets the resolution of this ProxyProfile.  # noqa: E501


        :return: The resolution of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """Sets the resolution of this ProxyProfile.


        :param resolution: The resolution of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                resolution is not None and len(resolution) > 1023):
            raise ValueError("Invalid value for `resolution`, length must be less than or equal to `1023`")  # noqa: E501

        self._resolution = resolution

    @property
    def rate_control(self):
        """Gets the rate_control of this ProxyProfile.  # noqa: E501


        :return: The rate_control of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._rate_control

    @rate_control.setter
    def rate_control(self, rate_control):
        """Sets the rate_control of this ProxyProfile.


        :param rate_control: The rate_control of this ProxyProfile.  # noqa: E501
        :type: int
        """

        self._rate_control = rate_control

    @property
    def crf(self):
        """Gets the crf of this ProxyProfile.  # noqa: E501


        :return: The crf of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._crf

    @crf.setter
    def crf(self, crf):
        """Sets the crf of this ProxyProfile.


        :param crf: The crf of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                crf is not None and crf > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `crf`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                crf is not None and crf < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `crf`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._crf = crf

    @property
    def bitrate(self):
        """Gets the bitrate of this ProxyProfile.  # noqa: E501


        :return: The bitrate of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._bitrate

    @bitrate.setter
    def bitrate(self, bitrate):
        """Sets the bitrate of this ProxyProfile.


        :param bitrate: The bitrate of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                bitrate is not None and bitrate > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `bitrate`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                bitrate is not None and bitrate < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `bitrate`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._bitrate = bitrate

    @property
    def audio_bitrate(self):
        """Gets the audio_bitrate of this ProxyProfile.  # noqa: E501


        :return: The audio_bitrate of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._audio_bitrate

    @audio_bitrate.setter
    def audio_bitrate(self, audio_bitrate):
        """Sets the audio_bitrate of this ProxyProfile.


        :param audio_bitrate: The audio_bitrate of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                audio_bitrate is not None and audio_bitrate > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `audio_bitrate`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                audio_bitrate is not None and audio_bitrate < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `audio_bitrate`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._audio_bitrate = audio_bitrate

    @property
    def variants_limit(self):
        """Gets the variants_limit of this ProxyProfile.  # noqa: E501


        :return: The variants_limit of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._variants_limit

    @variants_limit.setter
    def variants_limit(self, variants_limit):
        """Sets the variants_limit of this ProxyProfile.


        :param variants_limit: The variants_limit of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                variants_limit is not None and variants_limit > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `variants_limit`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                variants_limit is not None and variants_limit < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `variants_limit`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._variants_limit = variants_limit

    @property
    def enable_realtime_read(self):
        """Gets the enable_realtime_read of this ProxyProfile.  # noqa: E501


        :return: The enable_realtime_read of this ProxyProfile.  # noqa: E501
        :rtype: bool
        """
        return self._enable_realtime_read

    @enable_realtime_read.setter
    def enable_realtime_read(self, enable_realtime_read):
        """Sets the enable_realtime_read of this ProxyProfile.


        :param enable_realtime_read: The enable_realtime_read of this ProxyProfile.  # noqa: E501
        :type: bool
        """

        self._enable_realtime_read = enable_realtime_read

    @property
    def enable_dense_filmstrip(self):
        """Gets the enable_dense_filmstrip of this ProxyProfile.  # noqa: E501


        :return: The enable_dense_filmstrip of this ProxyProfile.  # noqa: E501
        :rtype: bool
        """
        return self._enable_dense_filmstrip

    @enable_dense_filmstrip.setter
    def enable_dense_filmstrip(self, enable_dense_filmstrip):
        """Sets the enable_dense_filmstrip of this ProxyProfile.


        :param enable_dense_filmstrip: The enable_dense_filmstrip of this ProxyProfile.  # noqa: E501
        :type: bool
        """

        self._enable_dense_filmstrip = enable_dense_filmstrip

    @property
    def enable_watermark(self):
        """Gets the enable_watermark of this ProxyProfile.  # noqa: E501


        :return: The enable_watermark of this ProxyProfile.  # noqa: E501
        :rtype: bool
        """
        return self._enable_watermark

    @enable_watermark.setter
    def enable_watermark(self, enable_watermark):
        """Sets the enable_watermark of this ProxyProfile.


        :param enable_watermark: The enable_watermark of this ProxyProfile.  # noqa: E501
        :type: bool
        """

        self._enable_watermark = enable_watermark

    @property
    def watermark_image(self):
        """Gets the watermark_image of this ProxyProfile.  # noqa: E501


        :return: The watermark_image of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._watermark_image

    @watermark_image.setter
    def watermark_image(self, watermark_image):
        """Sets the watermark_image of this ProxyProfile.


        :param watermark_image: The watermark_image of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                watermark_image is not None and len(watermark_image) > 1023):
            raise ValueError("Invalid value for `watermark_image`, length must be less than or equal to `1023`")  # noqa: E501

        self._watermark_image = watermark_image

    @property
    def watermark_position(self):
        """Gets the watermark_position of this ProxyProfile.  # noqa: E501


        :return: The watermark_position of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._watermark_position

    @watermark_position.setter
    def watermark_position(self, watermark_position):
        """Sets the watermark_position of this ProxyProfile.


        :param watermark_position: The watermark_position of this ProxyProfile.  # noqa: E501
        :type: int
        """

        self._watermark_position = watermark_position

    @property
    def watermark_opacity(self):
        """Gets the watermark_opacity of this ProxyProfile.  # noqa: E501


        :return: The watermark_opacity of this ProxyProfile.  # noqa: E501
        :rtype: float
        """
        return self._watermark_opacity

    @watermark_opacity.setter
    def watermark_opacity(self, watermark_opacity):
        """Sets the watermark_opacity of this ProxyProfile.


        :param watermark_opacity: The watermark_opacity of this ProxyProfile.  # noqa: E501
        :type: float
        """

        self._watermark_opacity = watermark_opacity

    @property
    def watermark_size(self):
        """Gets the watermark_size of this ProxyProfile.  # noqa: E501


        :return: The watermark_size of this ProxyProfile.  # noqa: E501
        :rtype: float
        """
        return self._watermark_size

    @watermark_size.setter
    def watermark_size(self, watermark_size):
        """Sets the watermark_size of this ProxyProfile.


        :param watermark_size: The watermark_size of this ProxyProfile.  # noqa: E501
        :type: float
        """

        self._watermark_size = watermark_size

    @property
    def enable_timecode(self):
        """Gets the enable_timecode of this ProxyProfile.  # noqa: E501


        :return: The enable_timecode of this ProxyProfile.  # noqa: E501
        :rtype: bool
        """
        return self._enable_timecode

    @enable_timecode.setter
    def enable_timecode(self, enable_timecode):
        """Sets the enable_timecode of this ProxyProfile.


        :param enable_timecode: The enable_timecode of this ProxyProfile.  # noqa: E501
        :type: bool
        """

        self._enable_timecode = enable_timecode

    @property
    def timecode_position(self):
        """Gets the timecode_position of this ProxyProfile.  # noqa: E501


        :return: The timecode_position of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._timecode_position

    @timecode_position.setter
    def timecode_position(self, timecode_position):
        """Sets the timecode_position of this ProxyProfile.


        :param timecode_position: The timecode_position of this ProxyProfile.  # noqa: E501
        :type: int
        """

        self._timecode_position = timecode_position

    @property
    def timecode_opacity(self):
        """Gets the timecode_opacity of this ProxyProfile.  # noqa: E501


        :return: The timecode_opacity of this ProxyProfile.  # noqa: E501
        :rtype: float
        """
        return self._timecode_opacity

    @timecode_opacity.setter
    def timecode_opacity(self, timecode_opacity):
        """Sets the timecode_opacity of this ProxyProfile.


        :param timecode_opacity: The timecode_opacity of this ProxyProfile.  # noqa: E501
        :type: float
        """

        self._timecode_opacity = timecode_opacity

    @property
    def timecode_size(self):
        """Gets the timecode_size of this ProxyProfile.  # noqa: E501


        :return: The timecode_size of this ProxyProfile.  # noqa: E501
        :rtype: float
        """
        return self._timecode_size

    @timecode_size.setter
    def timecode_size(self, timecode_size):
        """Sets the timecode_size of this ProxyProfile.


        :param timecode_size: The timecode_size of this ProxyProfile.  # noqa: E501
        :type: float
        """

        self._timecode_size = timecode_size

    @property
    def lut(self):
        """Gets the lut of this ProxyProfile.  # noqa: E501


        :return: The lut of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._lut

    @lut.setter
    def lut(self, lut):
        """Sets the lut of this ProxyProfile.


        :param lut: The lut of this ProxyProfile.  # noqa: E501
        :type: str
        """

        self._lut = lut

    @property
    def hotfolder_copy_to(self):
        """Gets the hotfolder_copy_to of this ProxyProfile.  # noqa: E501


        :return: The hotfolder_copy_to of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._hotfolder_copy_to

    @hotfolder_copy_to.setter
    def hotfolder_copy_to(self, hotfolder_copy_to):
        """Sets the hotfolder_copy_to of this ProxyProfile.


        :param hotfolder_copy_to: The hotfolder_copy_to of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_copy_to is not None and len(hotfolder_copy_to) > 1023):
            raise ValueError("Invalid value for `hotfolder_copy_to`, length must be less than or equal to `1023`")  # noqa: E501

        self._hotfolder_copy_to = hotfolder_copy_to

    @property
    def hotfolder_read_from(self):
        """Gets the hotfolder_read_from of this ProxyProfile.  # noqa: E501


        :return: The hotfolder_read_from of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._hotfolder_read_from

    @hotfolder_read_from.setter
    def hotfolder_read_from(self, hotfolder_read_from):
        """Sets the hotfolder_read_from of this ProxyProfile.


        :param hotfolder_read_from: The hotfolder_read_from of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_read_from is not None and len(hotfolder_read_from) > 1023):
            raise ValueError("Invalid value for `hotfolder_read_from`, length must be less than or equal to `1023`")  # noqa: E501

        self._hotfolder_read_from = hotfolder_read_from

    @property
    def hotfolder_queue_timeout(self):
        """Gets the hotfolder_queue_timeout of this ProxyProfile.  # noqa: E501


        :return: The hotfolder_queue_timeout of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._hotfolder_queue_timeout

    @hotfolder_queue_timeout.setter
    def hotfolder_queue_timeout(self, hotfolder_queue_timeout):
        """Sets the hotfolder_queue_timeout of this ProxyProfile.


        :param hotfolder_queue_timeout: The hotfolder_queue_timeout of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_queue_timeout is not None and hotfolder_queue_timeout > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `hotfolder_queue_timeout`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_queue_timeout is not None and hotfolder_queue_timeout < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `hotfolder_queue_timeout`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._hotfolder_queue_timeout = hotfolder_queue_timeout

    @property
    def hotfolder_encode_timeout(self):
        """Gets the hotfolder_encode_timeout of this ProxyProfile.  # noqa: E501


        :return: The hotfolder_encode_timeout of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._hotfolder_encode_timeout

    @hotfolder_encode_timeout.setter
    def hotfolder_encode_timeout(self, hotfolder_encode_timeout):
        """Sets the hotfolder_encode_timeout of this ProxyProfile.


        :param hotfolder_encode_timeout: The hotfolder_encode_timeout of this ProxyProfile.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_encode_timeout is not None and hotfolder_encode_timeout > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `hotfolder_encode_timeout`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                hotfolder_encode_timeout is not None and hotfolder_encode_timeout < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `hotfolder_encode_timeout`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._hotfolder_encode_timeout = hotfolder_encode_timeout

    @property
    def vantage_workflow_id(self):
        """Gets the vantage_workflow_id of this ProxyProfile.  # noqa: E501


        :return: The vantage_workflow_id of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._vantage_workflow_id

    @vantage_workflow_id.setter
    def vantage_workflow_id(self, vantage_workflow_id):
        """Sets the vantage_workflow_id of this ProxyProfile.


        :param vantage_workflow_id: The vantage_workflow_id of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                vantage_workflow_id is not None and len(vantage_workflow_id) > 63):
            raise ValueError("Invalid value for `vantage_workflow_id`, length must be less than or equal to `63`")  # noqa: E501

        self._vantage_workflow_id = vantage_workflow_id

    @property
    def external_transcoder_staging_path(self):
        """Gets the external_transcoder_staging_path of this ProxyProfile.  # noqa: E501


        :return: The external_transcoder_staging_path of this ProxyProfile.  # noqa: E501
        :rtype: str
        """
        return self._external_transcoder_staging_path

    @external_transcoder_staging_path.setter
    def external_transcoder_staging_path(self, external_transcoder_staging_path):
        """Sets the external_transcoder_staging_path of this ProxyProfile.


        :param external_transcoder_staging_path: The external_transcoder_staging_path of this ProxyProfile.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                external_transcoder_staging_path is not None and len(external_transcoder_staging_path) > 1023):
            raise ValueError("Invalid value for `external_transcoder_staging_path`, length must be less than or equal to `1023`")  # noqa: E501

        self._external_transcoder_staging_path = external_transcoder_staging_path

    @property
    def external_transcoder(self):
        """Gets the external_transcoder of this ProxyProfile.  # noqa: E501


        :return: The external_transcoder of this ProxyProfile.  # noqa: E501
        :rtype: int
        """
        return self._external_transcoder

    @external_transcoder.setter
    def external_transcoder(self, external_transcoder):
        """Sets the external_transcoder of this ProxyProfile.


        :param external_transcoder: The external_transcoder of this ProxyProfile.  # noqa: E501
        :type: int
        """

        self._external_transcoder = external_transcoder

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
        if not isinstance(other, ProxyProfile):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProxyProfile):
            return True

        return self.to_dict() != other.to_dict()
