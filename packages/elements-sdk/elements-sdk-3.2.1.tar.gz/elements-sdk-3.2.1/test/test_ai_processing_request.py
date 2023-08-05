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
from elements_sdk.models.ai_processing_request import AIProcessingRequest  # noqa: E501
from elements_sdk.rest import ApiException

class TestAIProcessingRequest(unittest.TestCase):
    """AIProcessingRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AIProcessingRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.ai_processing_request.AIProcessingRequest()  # noqa: E501
        if include_optional :
            return AIProcessingRequest(
                assets = [
                    56
                    ], 
                directories = [
                    56
                    ], 
                datasets = [
                    '0'
                    ], 
                preferred_proxy_profile = 56
            )
        else :
            return AIProcessingRequest(
                datasets = [
                    '0'
                    ],
        )

    def testAIProcessingRequest(self):
        """Test AIProcessingRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
