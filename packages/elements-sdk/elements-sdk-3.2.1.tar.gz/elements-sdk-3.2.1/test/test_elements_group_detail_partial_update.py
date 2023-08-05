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
from elements_sdk.models.elements_group_detail_partial_update import ElementsGroupDetailPartialUpdate  # noqa: E501
from elements_sdk.rest import ApiException

class TestElementsGroupDetailPartialUpdate(unittest.TestCase):
    """ElementsGroupDetailPartialUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ElementsGroupDetailPartialUpdate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = elements_sdk.models.elements_group_detail_partial_update.ElementsGroupDetailPartialUpdate()  # noqa: E501
        if include_optional :
            return ElementsGroupDetailPartialUpdate(
                permissions = [
                    '0'
                    ], 
                members = [
                    elements_sdk.models.elements_user.ElementsUser(
                        id = 56, 
                        allow_changing_password = True, 
                        allow_wan_login = True, 
                        allowed_fs_paths = [
                            '0'
                            ], 
                        allowed_fs_write_paths = [
                            '0'
                            ], 
                        avatar = '0', 
                        client_sessions = [
                            elements_sdk.models.client_session.ClientSession(
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
                                mounted_workspaces = [
                                    elements_sdk.models.mounted_workspace.MountedWorkspace(
                                        id = 56, 
                                        workspace = elements_sdk.models.workspace.Workspace(
                                            id = 56, 
                                            name = '0', 
                                            production = elements_sdk.models.production.Production(
                                                id = 56, 
                                                name = '0', ), ), 
                                        mountpoint = '0', 
                                        address = '0', 
                                        protocol = '0', 
                                        last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        user = 56, 
                                        client_session = 56, )
                                    ], 
                                started = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                workstation = '0', )
                            ], 
                        default_page = '0', 
                        display_name = '0', 
                        effective_permissions = [
                            '0'
                            ], 
                        email = '0', 
                        expiry = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        ancillary_path_read_only = True, 
                        ancillary_path = '0', 
                        fm_bookmarks = [
                            '0'
                            ], 
                        full_name = '0', 
                        gid = -2147483648, 
                        group_permissions = [
                            '0'
                            ], 
                        has_password = True, 
                        home = 56, 
                        is_anonymous = '0', 
                        is_cloud = True, 
                        is_cloud_default = True, 
                        is_enabled = True, 
                        language = 'en', 
                        last_seen = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        ldap = 56, 
                        ldap_dn = '0', 
                        password_change_required = True, 
                        permissions = [
                            '0'
                            ], 
                        shaper_ceiling = -9223372036854775808, 
                        shaper_rate = -9223372036854775808, 
                        sync_id = '0', 
                        totp_enabled = True, 
                        uid = -2147483648, 
                        unix_username = '0', 
                        username = '0', )
                    ], 
                ldap = elements_sdk.models.ldap_server.LDAPServer(
                    id = 56, 
                    name = '0', 
                    winbind_separator = '0', 
                    nt_domain = '0', ), 
                name = '0', 
                ldap_dn = '0', 
                unix_groupname = '0', 
                gid = -2147483648, 
                ancillary_path = '0', 
                ancillary_path_read_only = True
            )
        else :
            return ElementsGroupDetailPartialUpdate(
        )

    def testElementsGroupDetailPartialUpdate(self):
        """Test ElementsGroupDetailPartialUpdate"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
