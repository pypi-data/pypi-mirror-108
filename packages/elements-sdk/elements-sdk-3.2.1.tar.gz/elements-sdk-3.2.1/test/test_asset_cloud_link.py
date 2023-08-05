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
from elements_sdk.models.asset_cloud_link import AssetCloudLink  # noqa: E501
from elements_sdk.rest import ApiException

class TestAssetCloudLink(unittest.TestCase):
    """AssetCloudLink unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AssetCloudLink
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.asset_cloud_link.AssetCloudLink()  # noqa: E501
        if include_optional :
            return AssetCloudLink(
                id = 56, 
                connection = elements_sdk.models.connection.Connection(
                    id = 56, 
                    name = '0', 
                    url = '0', 
                    presigned_login_url = '0', ), 
                presigned_asset_url = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                asset = 56
            )
        else :
            return AssetCloudLink(
                asset = 56,
        )

    def testAssetCloudLink(self):
        """Test AssetCloudLink"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
