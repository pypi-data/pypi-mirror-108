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
from elements_sdk.models.register_upload_endpoint_request import RegisterUploadEndpointRequest  # noqa: E501
from elements_sdk.rest import ApiException

class TestRegisterUploadEndpointRequest(unittest.TestCase):
    """RegisterUploadEndpointRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RegisterUploadEndpointRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.register_upload_endpoint_request.RegisterUploadEndpointRequest()  # noqa: E501
        if include_optional :
            return RegisterUploadEndpointRequest(
                upload_id = '0', 
                path = '0'
            )
        else :
            return RegisterUploadEndpointRequest(
                upload_id = '0',
                path = '0',
        )

    def testRegisterUploadEndpointRequest(self):
        """Test RegisterUploadEndpointRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
