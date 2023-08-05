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
from elements_sdk.models.media_file_bundle import MediaFileBundle  # noqa: E501
from elements_sdk.rest import ApiException

class TestMediaFileBundle(unittest.TestCase):
    """MediaFileBundle unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MediaFileBundle
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.media_file_bundle.MediaFileBundle()  # noqa: E501
        if include_optional :
            return MediaFileBundle(
                id = 56, 
                asset = elements_sdk.models.asset.Asset(
                    id = 56, 
                    urls = elements_sdk.models.urls.Urls(
                        id = 56, 
                        profile = elements_sdk.models.profile.Profile(
                            id = 56, 
                            name = '0', ), 
                        failed_reason = '0', 
                        generated = True, 
                        failed = True, 
                        name = '0', 
                        variant_id = 'default', 
                        variant_config = '0', 
                        asset = 56, ), 
                    proxies = [
                        elements_sdk.models.urls.Urls(
                            id = 56, 
                            failed_reason = '0', 
                            generated = True, 
                            failed = True, 
                            name = '0', 
                            variant_id = 'default', 
                            variant_config = '0', 
                            asset = 56, )
                        ], 
                    default_proxy = elements_sdk.models.urls.Urls(
                        id = 56, 
                        failed_reason = '0', 
                        generated = True, 
                        failed = True, 
                        name = '0', 
                        variant_id = 'default', 
                        variant_config = '0', 
                        asset = 56, ), 
                    info = {
                        'key' : '0'
                        }, 
                    proxy_info = {
                        'key' : '0'
                        }, 
                    custom_fields = {
                        'key' : '0'
                        }, 
                    tags = [
                        elements_sdk.models.tag.Tag(
                            id = 56, 
                            name = '0', 
                            color = '0', 
                            root = 56, )
                        ], 
                    resolved_permission = elements_sdk.models.resolved_permission.Resolved permission(
                        id = 56, 
                        user = elements_sdk.models.elements_user_mini.ElementsUserMini(
                            id = 56, 
                            avatar = '0', 
                            display_name = '0', 
                            email = '0', 
                            full_name = '0', 
                            is_anonymous = '0', 
                            is_cloud = True, 
                            username = '0', ), 
                        group = elements_sdk.models.elements_group.ElementsGroup(
                            id = 56, 
                            permissions = [
                                '0'
                                ], 
                            members_preview = [
                                elements_sdk.models.member_preview.MemberPreview(
                                    id = 56, 
                                    avatar = '0', 
                                    email = '0', )
                                ], 
                            effective_permissions = [
                                '0'
                                ], 
                            name = '0', 
                            ldap_dn = '0', 
                            unix_groupname = '0', 
                            gid = -2147483648, 
                            ancillary_path = '0', 
                            ancillary_path_read_only = True, 
                            ldap = 56, 
                            members = [
                                56
                                ], ), 
                        full_path = '0', 
                        path = '0', 
                        allow_create = True, 
                        allow_write_fs = True, 
                        allow_write_db = True, 
                        allow_proxy_download = True, 
                        allow_original_download = True, 
                        allow_upload = True, 
                        allow_sharing = True, 
                        allow_delete_fs = True, 
                        allow_delete_db = True, 
                        show_tags = True, 
                        show_comments = True, 
                        show_locations = True, 
                        show_custom_fields = True, 
                        show_ratings = True, 
                        show_subclips = True, 
                        show_ai_metadata = True, 
                        show_markers = True, 
                        root = 56, ), 
                    bundles = '0', 
                    backups = '0', 
                    proxies_generated = True, 
                    proxies_failed = True, 
                    modified_by = elements_sdk.models.elements_user_mini.ElementsUserMini(
                        id = 56, 
                        avatar = '0', 
                        display_name = '0', 
                        email = '0', 
                        full_name = '0', 
                        is_anonymous = '0', 
                        is_cloud = True, 
                        username = '0', ), 
                    sync_id = '0', 
                    display_name = '0', 
                    has_files = True, 
                    has_backups = True, 
                    has_cloud_links = True, 
                    checksum = '0', 
                    type = '0', 
                    thumbnail_generated = True, 
                    matched_scanner = '0', 
                    rating = 1.337, 
                    workflow_state = 56, 
                    is_temporary = True, 
                    created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    set = 56, ), 
                mainfile = elements_sdk.models.mainfile.Mainfile(
                    id = 56, 
                    name = '0', 
                    bundle = 56, 
                    full_path = '0', 
                    custom_fields = elements_sdk.models.custom_fields.Custom fields(), 
                    mtime = 56, 
                    parent = '0', 
                    path = '0', 
                    present = True, 
                    size = 56, 
                    volume = elements_sdk.models.volume.Volume(
                        id = 56, 
                        name = '0', 
                        path = '0', 
                        display_name = '0', 
                        visual_tag = '0', 
                        type = 'generic', ), ), 
                snm_attributes = elements_sdk.models.snm_attributes.Snm attributes(
                    location = '0', 
                    policy_class = '0', 
                    existing_copies = 56, 
                    target_copies = 56, ), 
                search_highlight = '0', 
                name = '0', 
                location = 56
            )
        else :
            return MediaFileBundle(
                name = '0',
                location = 56,
        )

    def testMediaFileBundle(self):
        """Test MediaFileBundle"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
