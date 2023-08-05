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
from elements_sdk.models.multiple_assets_request import MultipleAssetsRequest  # noqa: E501
from elements_sdk.rest import ApiException

class TestMultipleAssetsRequest(unittest.TestCase):
    """MultipleAssetsRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MultipleAssetsRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.multiple_assets_request.MultipleAssetsRequest()  # noqa: E501
        if include_optional :
            return MultipleAssetsRequest(
                assets = [
                    56
                    ]
            )
        else :
            return MultipleAssetsRequest(
                assets = [
                    56
                    ],
        )

    def testMultipleAssetsRequest(self):
        """Test MultipleAssetsRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
