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
from elements_sdk.models.external_transcoder_partial_update import ExternalTranscoderPartialUpdate  # noqa: E501
from elements_sdk.rest import ApiException

class TestExternalTranscoderPartialUpdate(unittest.TestCase):
    """ExternalTranscoderPartialUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ExternalTranscoderPartialUpdate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.external_transcoder_partial_update.ExternalTranscoderPartialUpdate()  # noqa: E501
        if include_optional :
            return ExternalTranscoderPartialUpdate(
                path_mappings = [
                    '0'
                    ], 
                name = '0', 
                type = 'transkoder', 
                address = '0'
            )
        else :
            return ExternalTranscoderPartialUpdate(
        )

    def testExternalTranscoderPartialUpdate(self):
        """Test ExternalTranscoderPartialUpdate"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
