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
from elements_sdk.models.proxy_count import ProxyCount  # noqa: E501
from elements_sdk.rest import ApiException

class TestProxyCount(unittest.TestCase):
    """ProxyCount unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ProxyCount
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.proxy_count.ProxyCount()  # noqa: E501
        if include_optional :
            return ProxyCount(
                count = 56
            )
        else :
            return ProxyCount(
                count = 56,
        )

    def testProxyCount(self):
        """Test ProxyCount"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
