# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_options.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOptions
from ramstk.dao import DAO
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.models.programdb import RAMSTKProgramInfo


@pytest.mark.usefixtures('test_program_dao', 'test_common_dao',
                         'test_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self, test_program_dao, test_common_dao):
        """__init__() should return a Options data manager."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)

        assert isinstance(DUT, dmOptions)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, DAO)
        assert isinstance(DUT.common_dao, DAO)
        assert DUT._tag == 'options'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'request_select_options')
        assert pub.isSubscribed(DUT.do_update, 'request_update_option')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_option_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_options_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_option_attributes')


@pytest.mark.usefixtures('test_program_dao', 'test_common_dao',
                         'test_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_options(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node('programinfo').data['programinfo'],
            RAMSTKProgramInfo)
        assert isinstance(
            tree.get_node('siteinfo').data['siteinfo'], RAMSTKSiteInfo)
        print("\033[36m\nsucceed_retrieve_options topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all(self, test_program_dao, test_common_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        pub.subscribe(self.on_succeed_retrieve_options,
                      'succeed_retrieve_options')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        assert isinstance(
            DUT.tree.get_node('programinfo').data['programinfo'],
            RAMSTKProgramInfo)
        assert isinstance(
            DUT.tree.get_node('siteinfo').data['siteinfo'], RAMSTKSiteInfo)

        pub.unsubscribe(self.on_succeed_retrieve_options,
                        'succeed_retrieve_options')

    @pytest.mark.integration
    def test_do_select_site_info(self, test_program_dao, test_common_dao):
        """do_select() should return an instance of the RAMSTKSiteInfo on success."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        _options = DUT.do_select('siteinfo', table='siteinfo')

        assert isinstance(_options, RAMSTKSiteInfo)
        assert _options.function_enabled == 0
        assert _options.requirement_enabled == 0
        assert _options.hardware_enabled == 0
        assert _options.vandv_enabled == 0
        assert _options.fmea_enabled == 0

    @pytest.mark.integration
    def test_do_select_program_info(self, test_program_dao, test_common_dao):
        """do_select() should return an instance of the RAMSTKProgramInfo on success."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        _options = DUT.do_select('programinfo', table='programinfo')

        assert isinstance(_options, RAMSTKProgramInfo)
        assert _options.function_active == 1
        assert _options.requirement_active == 1
        assert _options.hardware_active == 1
        assert _options.software_active == 1
        assert _options.vandv_active == 1
        assert _options.fmea_active == 1
        assert _options.testing_active == 1
        assert _options.fraca_active == 1
        assert _options.survival_active == 1
        assert _options.rcm_active == 0
        assert _options.rbd_active == 0
        assert _options.fta_active == 0
        assert _options.created_on == date(2019, 7, 21)
        assert _options.created_by == ''
        assert _options.last_saved == date(2019, 7, 21)
        assert _options.last_saved_by == ''
        assert _options.method == 'STANDARD'

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao,
                                       test_common_dao):
        """do_select() should return None when a non-existent Options ID is requested."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        assert DUT.do_select(100, table='siteinfo') is None


@pytest.mark.usefixtures('test_program_dao', 'test_common_dao',
                         'test_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_site_info_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_enabled'] == 0
        assert attributes['requirement_enabled'] == 0
        assert attributes['hardware_enabled'] == 0
        assert attributes['vandv_enabled'] == 0
        assert attributes['fmea_enabled'] == 0
        print("\033[36m\nsucceed_get_siteinfo_attributes topic was broadcast.")

    def on_succeed_get_program_info_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_active'] == 1
        assert attributes['requirement_active'] == 1
        assert attributes['hardware_active'] == 1
        assert attributes['software_active'] == 1
        assert attributes['vandv_active'] == 1
        assert attributes['fmea_active'] == 1
        assert attributes['testing_active'] == 1
        assert attributes['fraca_active'] == 1
        assert attributes['survival_active'] == 1
        assert attributes['rcm_active'] == 0
        assert attributes['rbd_active'] == 0
        assert attributes['fta_active'] == 0
        assert attributes['created_on'] == date(2019, 7, 21)
        assert attributes['created_by'] == ''
        assert attributes['last_saved'] == date(2019, 7, 21)
        assert attributes['last_saved_by'] == ''
        assert attributes['method'] == 'STANDARD'
        print(
            "\033[36m\nsucceed_get_programinfo_attributes topic was broadcast."
        )

    def on_succeed_get_options_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(
            dmtree.get_node('siteinfo').data['siteinfo'], RAMSTKSiteInfo)
        assert isinstance(
            dmtree.get_node('programinfo').data['programinfo'],
            RAMSTKProgramInfo)
        print("\033[36m\nsucceed_get_options_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_site_info_attributes(self, test_program_dao,
                                         test_common_dao):
        """do_get_attributes() should return a dict of site information attributes on success."""
        pub.subscribe(self.on_succeed_get_site_info_attrs,
                      'succeed_get_siteinfo_attributes')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)
        DUT.do_get_attributes('siteinfo', 'siteinfo')

        assert isinstance(
            DUT.tree.get_node('siteinfo').data['siteinfo'], RAMSTKSiteInfo)

        pub.unsubscribe(self.on_succeed_get_site_info_attrs,
                        'succeed_get_siteinfo_attributes')

    @pytest.mark.integration
    def test_do_get_program_info_attributes(self, test_program_dao,
                                            test_common_dao):
        """do_get_attributes() should return a dict of program information attributes on success."""
        pub.subscribe(self.on_succeed_get_program_info_attrs,
                      'succeed_get_programinfo_attributes')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)
        DUT.do_get_attributes('programinfo', 'programinfo')

        assert isinstance(
            DUT.tree.get_node('programinfo').data['programinfo'],
            RAMSTKProgramInfo)

        pub.unsubscribe(self.on_succeed_get_program_info_attrs,
                        'succeed_get_programinfo_attributes')

    @pytest.mark.integration
    def test_do_set_site_info_attributes(self, test_program_dao,
                                         test_common_dao):
        """do_set_attributes() should return None when successfully setting site information attributes."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        pub.sendMessage('request_set_option_attributes',
                        node_id='siteinfo',
                        key='function_enabled',
                        value=1,
                        table='siteinfo')
        pub.sendMessage('request_set_option_attributes',
                        node_id='siteinfo',
                        key='requirement_enabled',
                        value=1,
                        table='siteinfo')
        assert DUT.do_select('siteinfo',
                             table='siteinfo').function_enabled == 1
        assert DUT.do_select('siteinfo',
                             table='siteinfo').requirement_enabled == 1

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_option_attributes')

    @pytest.mark.integration
    def test_do_set_program_info_attributes(self, test_program_dao,
                                            test_common_dao):
        """do_set_attributes() should return None when successfully setting program information attributes."""
        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        pub.sendMessage('request_set_option_attributes',
                        node_id='programinfo',
                        key='function_active',
                        value=0,
                        table='programinfo')
        pub.sendMessage('request_set_option_attributes',
                        node_id='programinfo',
                        key='rcm_active',
                        value=1,
                        table='programinfo')
        assert DUT.do_select('programinfo',
                             table='programinfo').function_active == 0
        assert DUT.do_select('programinfo',
                             table='programinfo').rcm_active == 1

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_option_attributes')

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_program_dao, test_common_dao):
        """on_get_tree() should return the Options treelib Tree."""
        pub.subscribe(self.on_succeed_get_options_tree,
                      'succeed_get_options_tree')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_options_tree,
                        'succeed_get_options_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_common_dao',
                         'test_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_options(self, node_id):
        assert node_id == 'siteinfo'
        print("\033[36m\nsucceed_update_options topic was broadcast")

    def on_fail_update_options(self, error_msg):
        assert error_msg == (
            'Attempted to save non-existent Option with Options ID 100.')
        print("\033[35m\nfail_update_options topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao, test_common_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_options, 'succeed_update_options')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)

        DUT.tree.get_node('siteinfo').data['siteinfo'].hardware_enabled = 1
        DUT.tree.get_node('siteinfo').data['siteinfo'].vandv_enabled = 1
        DUT.do_update('siteinfo')

        pub.unsubscribe(self.on_succeed_update_options,
                        'succeed_update_options')

        DUT.tree.get_node('programinfo').data['programinfo'].hardware_active = 0
        DUT.tree.get_node('programinfo').data['programinfo'].vandv_active = 0
        DUT.do_update('programinfo')

        DUT.do_select_all(1)
        assert DUT.tree.get_node(
            'siteinfo').data['siteinfo'].hardware_enabled == 1
        assert DUT.tree.get_node(
            'siteinfo').data['siteinfo'].vandv_enabled == 1
        assert DUT.tree.get_node(
            'programinfo').data['programinfo'].hardware_active == 0
        assert DUT.tree.get_node(
            'programinfo').data['programinfo'].vandv_active == 0

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao,
                                       test_common_dao):
        """ do_update() should return a non-zero error code when passed a Options ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_options, 'fail_update_options')

        DUT = dmOptions(test_program_dao, common_dao=test_common_dao)
        DUT.do_select_all(1)
        DUT.do_update('100')

        pub.unsubscribe(self.on_fail_update_options, 'fail_update_options')
