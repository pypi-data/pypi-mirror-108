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
from elements_sdk.models.production_partial_update import ProductionPartialUpdate  # noqa: E501
from elements_sdk.rest import ApiException

class TestProductionPartialUpdate(unittest.TestCase):
    """ProductionPartialUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ProductionPartialUpdate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.production_partial_update.ProductionPartialUpdate()  # noqa: E501
        if include_optional :
            return ProductionPartialUpdate(
                name = '0', 
                obscure_name = True, 
                description = '0', 
                long_description = '0', 
                active = True, 
                template = 56, 
                default_group = 56
            )
        else :
            return ProductionPartialUpdate(
        )

    def testProductionPartialUpdate(self):
        """Test ProductionPartialUpdate"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
