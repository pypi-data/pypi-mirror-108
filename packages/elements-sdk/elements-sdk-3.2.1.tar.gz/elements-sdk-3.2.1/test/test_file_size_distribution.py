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
from elements_sdk.models.file_size_distribution import FileSizeDistribution  # noqa: E501
from elements_sdk.rest import ApiException

class TestFileSizeDistribution(unittest.TestCase):
    """FileSizeDistribution unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test FileSizeDistribution
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.file_size_distribution.FileSizeDistribution()  # noqa: E501
        if include_optional :
            return FileSizeDistribution(
                distribution = [
                    elements_sdk.models.file_size_distribution_item.FileSizeDistributionItem(
                        min = 56, 
                        max = 56, 
                        count = 56, 
                        percent = 56, 
                        average = 56, 
                        total = 56, )
                    ]
            )
        else :
            return FileSizeDistribution(
                distribution = [
                    elements_sdk.models.file_size_distribution_item.FileSizeDistributionItem(
                        min = 56, 
                        max = 56, 
                        count = 56, 
                        percent = 56, 
                        average = 56, 
                        total = 56, )
                    ],
        )

    def testFileSizeDistribution(self):
        """Test FileSizeDistribution"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
