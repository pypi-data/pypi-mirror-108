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
from elements_sdk.models.custom_field import CustomField  # noqa: E501
from elements_sdk.rest import ApiException

class TestCustomField(unittest.TestCase):
    """CustomField unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CustomField
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.custom_field.CustomField()  # noqa: E501
        if include_optional :
            return CustomField(
                id = 56, 
                labels = [
                    '0'
                    ], 
                options = [
                    '0'
                    ], 
                name = '0', 
                order = -2147483648, 
                type = '0', 
                use_for_uploads = True, 
                require_to_upload = True, 
                non_user_editable = True, 
                validation = 'number_of_digits', 
                regex = '0', 
                range_min = -2147483648, 
                range_max = -2147483648, 
                number_of_digits = -2147483648, 
                metadata_prefill = '0', 
                highlight_expiration = True, 
                multiple_response = True
            )
        else :
            return CustomField(
                labels = [
                    '0'
                    ],
                options = [
                    '0'
                    ],
                name = '0',
                type = '0',
        )

    def testCustomField(self):
        """Test CustomField"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
