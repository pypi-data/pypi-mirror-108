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
from elements_sdk.models.ai_category_detail import AICategoryDetail  # noqa: E501
from elements_sdk.rest import ApiException

class TestAICategoryDetail(unittest.TestCase):
    """AICategoryDetail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AICategoryDetail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.ai_category_detail.AICategoryDetail()  # noqa: E501
        if include_optional :
            return AICategoryDetail(
                id = '0', 
                annotation_count = 56, 
                sample_annotation = elements_sdk.models.ai_annotation.AIAnnotation(
                    id = '0', 
                    relative_left = 1.337, 
                    relative_top = 1.337, 
                    relative_width = 1.337, 
                    relative_height = 1.337, 
                    track = '0', 
                    image = '0', 
                    category = '0', ), 
                connection = '0', 
                dataset = elements_sdk.models.ai_dataset.AIDataset(
                    id = '0', 
                    training_model = elements_sdk.models.training_model.Training model(
                        id = '0', 
                        state = 56, 
                        progress = elements_sdk.models.progress.Progress(
                            current_step = 56, 
                            total_steps = 56, 
                            eta = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        training_pid = -2147483648, 
                        dataset = '0', 
                        preprocessing_task = '0', ), 
                    last_finished_model = elements_sdk.models.training_model.Training model(
                        id = '0', 
                        state = 56, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        training_pid = -2147483648, 
                        dataset = '0', 
                        preprocessing_task = '0', ), 
                    last_change = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    name = '0', 
                    engine = '0', 
                    connection = 56, ), 
                name = '0'
            )
        else :
            return AICategoryDetail(
                dataset = elements_sdk.models.ai_dataset.AIDataset(
                    id = '0', 
                    training_model = elements_sdk.models.training_model.Training model(
                        id = '0', 
                        state = 56, 
                        progress = elements_sdk.models.progress.Progress(
                            current_step = 56, 
                            total_steps = 56, 
                            eta = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        training_pid = -2147483648, 
                        dataset = '0', 
                        preprocessing_task = '0', ), 
                    last_finished_model = elements_sdk.models.training_model.Training model(
                        id = '0', 
                        state = 56, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        training_pid = -2147483648, 
                        dataset = '0', 
                        preprocessing_task = '0', ), 
                    last_change = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    name = '0', 
                    engine = '0', 
                    connection = 56, ),
                name = '0',
        )

    def testAICategoryDetail(self):
        """Test AICategoryDetail"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
