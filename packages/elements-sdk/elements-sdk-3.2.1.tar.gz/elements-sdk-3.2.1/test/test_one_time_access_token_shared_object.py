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
from elements_sdk.models.one_time_access_token_shared_object import OneTimeAccessTokenSharedObject  # noqa: E501
from elements_sdk.rest import ApiException

class TestOneTimeAccessTokenSharedObject(unittest.TestCase):
    """OneTimeAccessTokenSharedObject unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OneTimeAccessTokenSharedObject
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.one_time_access_token_shared_object.OneTimeAccessTokenSharedObject()  # noqa: E501
        if include_optional :
            return OneTimeAccessTokenSharedObject(
                id = 56, 
                name = '0'
            )
        else :
            return OneTimeAccessTokenSharedObject(
                id = 56,
                name = '0',
        )

    def testOneTimeAccessTokenSharedObject(self):
        """Test OneTimeAccessTokenSharedObject"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
