# coding: utf-8

"""
    ELEMENTS API

    The version of the OpenAPI document: 2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import elements_sdk
from elements_sdk.models.test_external_transcoder_connection_request import TestExternalTranscoderConnectionRequest  # noqa: E501
from elements_sdk.rest import ApiException

class TestTestExternalTranscoderConnectionRequest(unittest.TestCase):
    """TestExternalTranscoderConnectionRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TestExternalTranscoderConnectionRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.test_external_transcoder_connection_request.TestExternalTranscoderConnectionRequest()  # noqa: E501
        if include_optional :
            return TestExternalTranscoderConnectionRequest(
                type = '0', 
                address = '0'
            )
        else :
            return TestExternalTranscoderConnectionRequest(
                type = '0',
                address = '0',
        )

    def testTestExternalTranscoderConnectionRequest(self):
        """Test TestExternalTranscoderConnectionRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
