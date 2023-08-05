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
from elements_sdk.models.subtask import Subtask  # noqa: E501
from elements_sdk.rest import ApiException

class TestSubtask(unittest.TestCase):
    """Subtask unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Subtask
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.subtask.Subtask()  # noqa: E501
        if include_optional :
            return Subtask(
                id = 56, 
                kwargs = {
                    'key' : '0'
                    }, 
                validation_error = '0', 
                trigger = 'finish', 
                name = '0', 
                noop_dont_save = True, 
                no_concurrency = True, 
                log_variable = True, 
                task = '0', 
                condition_variable = '0', 
                condition_value = '0', 
                parent = 56, 
                relative_to = 56
            )
        else :
            return Subtask(
                kwargs = {
                    'key' : '0'
                    },
                parent = 56,
        )

    def testSubtask(self):
        """Test Subtask"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
