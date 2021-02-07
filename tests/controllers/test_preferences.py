# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_preferencess.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPreferences
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKProgramInfo


@pytest.fixture(scope="function")
def mock_program_dao(monkeypatch):
    _program_1 = RAMSTKProgramInfo()
    _program_1.revision_id = 1
    _program_1.function_active = 1
    _program_1.requirement_active = 1
    _program_1.hardware_active = 1
    _program_1.software_active = 0
    _program_1.rcm_active = 0
    _program_1.testing_active = 0
    _program_1.incident_active = 0
    _program_1.survival_active = 0
    _program_1.vandv_active = 1
    _program_1.hazard_active = 1
    _program_1.stakeholder_active = 1
    _program_1.allocation_active = 1
    _program_1.similar_item_active = 1
    _program_1.fmea_active = 1
    _program_1.pof_active = 1
    _program_1.rbd_active = 0
    _program_1.fta_active = 0
    _program_1.created_on = date.today()
    _program_1.created_by = ''
    _program_1.last_saved = date.today()
    _program_1.last_saved_by = ''

    DAO = MockDAO()
    DAO.table = [
        _program_1,
    ]

    yield DAO


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Options data manager."""
        DUT = dmPreferences()

        assert isinstance(DUT, dmPreferences)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._pkey == {
            'programinfo': ['revision_id'],
        }
        assert DUT._tag == 'preferences'
        assert DUT._root == 0

        assert pub.isSubscribed(DUT._do_select_all,
                                'succeed_connect_program_database')
        assert pub.isSubscribed(DUT.do_update, 'request_update_preference')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_preference_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_preferences_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_preference_attributes')


@pytest.mark.usefixtures('mock_program_dao')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_preferences(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['programinfo'], RAMSTKProgramInfo)
        print("\033[36m\nsucceed_retrieve_preferences topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        pub.subscribe(self.on_succeed_retrieve_preferences,
                      'succeed_retrieve_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        pub.unsubscribe(self.on_succeed_retrieve_preferences,
                        'succeed_retrieve_preferences')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing Preferences
        tree."""
        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        pub.subscribe(self.on_succeed_retrieve_preferences,
                      'succeed_retrieve_preferences')

        DUT._do_select_all(mock_program_dao)

        pub.unsubscribe(self.on_succeed_retrieve_preferences,
                        'succeed_retrieve_preferences')

    @pytest.mark.unit
    def test_do_select_program_info(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKProgramInfo on
        success."""
        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        _preferences = DUT.do_select(1, table='programinfo')

        assert isinstance(_preferences, RAMSTKProgramInfo)
        assert _preferences.function_active == 1
        assert _preferences.requirement_active == 1
        assert _preferences.hardware_active == 1
        assert _preferences.software_active == 0
        assert _preferences.rcm_active == 0
        assert _preferences.testing_active == 0
        assert _preferences.incident_active == 0
        assert _preferences.survival_active == 0
        assert _preferences.vandv_active == 1
        assert _preferences.hazard_active == 1
        assert _preferences.stakeholder_active == 1
        assert _preferences.allocation_active == 1
        assert _preferences.similar_item_active == 1
        assert _preferences.fmea_active == 1
        assert _preferences.pof_active == 1
        assert _preferences.rbd_active == 0
        assert _preferences.fta_active == 0
        assert _preferences.created_on == date.today()
        assert _preferences.created_by == ''
        assert _preferences.last_saved == date.today()
        assert _preferences.last_saved_by == ''

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        assert DUT.do_select(100, table='programinfo') is None


@pytest.mark.usefixtures('mock_program_dao')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_program_info_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_active'] == 1
        assert attributes['requirement_active'] == 1
        assert attributes['hardware_active'] == 1
        assert attributes['software_active'] == 0
        assert attributes['rcm_active'] == 0
        assert attributes['testing_active'] == 0
        assert attributes['incident_active'] == 0
        assert attributes['survival_active'] == 0
        assert attributes['vandv_active'] == 1
        assert attributes['hazard_active'] == 1
        assert attributes['stakeholder_active'] == 1
        assert attributes['allocation_active'] == 1
        assert attributes['similar_item_active'] == 1
        assert attributes['fmea_active'] == 1
        assert attributes['pof_active'] == 1
        assert attributes['rbd_active'] == 0
        assert attributes['fta_active'] == 0
        assert attributes['created_on'] == date.today()
        assert attributes['created_by'] == ''
        assert attributes['last_saved'] == date.today()
        assert attributes['last_saved_by'] == ''
        print(
            "\033[36m\nsucceed_get_programinfo_attributes topic was broadcast."
        )

    def on_succeed_get_preferences_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['programinfo'], RAMSTKProgramInfo)
        print("\033[36m\nsucceed_get_preferences_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_program_info_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of program information
        attributes on success."""
        pub.subscribe(self.on_succeed_get_program_info_attrs,
                      'succeed_get_programinfo_attributes')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)
        DUT.do_get_attributes(1, 'programinfo')

        assert isinstance(
            DUT.tree.get_node(1).data['programinfo'], RAMSTKProgramInfo)

        pub.unsubscribe(self.on_succeed_get_program_info_attrs,
                        'succeed_get_programinfo_attributes')

    @pytest.mark.unit
    def test_do_set_program_info_attributes(self, mock_program_dao):
        """do_set_attributes() should return None when successfully setting
        program information attributes."""
        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        pub.sendMessage('request_set_preference_attributes',
                        node_id=[1],
                        package={'function_active': 0})
        pub.sendMessage('request_set_preference_attributes',
                        node_id=[1],
                        package={'rcm_active': 1})
        assert DUT.do_select(1, table='programinfo').function_active == 0
        assert DUT.do_select(1, table='programinfo').rcm_active == 1

        pub.sendMessage('request_set_preference_attributes',
                        node_id=[1],
                        package={'function_active': 1})
        pub.sendMessage('request_set_preference_attributes',
                        node_id=[1],
                        package={'rcm_active': 0})
        assert DUT.do_select(1, table='programinfo').function_active == 1
        assert DUT.do_select(1, table='programinfo').rcm_active == 0

    @pytest.mark.unit
    def test_do_set_program_info_attributes_no_key(self, mock_program_dao):
        """do_set_attributes() should return None when successfully setting
        program information attributes."""
        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        pub.sendMessage('request_set_preference_attributes',
                        node_id=[1],
                        package={'cheesewhiz_active': 0})
        assert DUT.do_select(1, table='programinfo').requirement_active == 1

        pub.unsubscribe(DUT.do_set_attributes,
                        'request_set_preference_attributes')

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the Options treelib Tree."""
        pub.subscribe(self.on_succeed_get_preferences_tree,
                      'succeed_get_preferences_tree')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_preferences_tree,
                        'succeed_get_preferences_tree')


@pytest.mark.usefixtures('mock_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_preferences(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_preferences topic was broadcast")

    def on_fail_update_preferences_non_existent_id(self, error_message):
        assert error_message == ('do_update: Attempted to save non-existent '
                                 'Program ID skullduggery.')
        print("\033[35m\nfail_update_preferences topic was broadcast")

    def on_fail_update_preferences_no_data_package(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'Preference 1.')
        print("\033[35m\nfail_update_preferences topic was broadcast")

    def on_fail_update_preferences_wrong_data_type(self, error_message):
        assert error_message == ('do_update: The value for one or more '
                                 'attributes for Preferences 1 was the wrong '
                                 'type.')
        print("\033[35m\nfail_update_preferences topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_preferences,
                      'succeed_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)

        DUT.tree.get_node(1).data['programinfo'].hardware_active = 0
        DUT.tree.get_node(1).data['programinfo'].vandv_active = 0
        DUT.do_update(1)

        assert DUT.tree.get_node(1).data['programinfo'].hardware_active == 0
        assert DUT.tree.get_node(1).data['programinfo'].vandv_active == 0

        DUT.tree.get_node(1).data['programinfo'].hardware_active = 1
        DUT.tree.get_node(1).data['programinfo'].vandv_active = 1
        DUT.do_update(1)

        assert DUT.tree.get_node(1).data['programinfo'].hardware_active == 1
        assert DUT.tree.get_node(1).data['programinfo'].vandv_active == 1

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_preferences_non_existent_id,
                      'fail_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)
        DUT.do_update('skullduggery')

        pub.unsubscribe(self.on_fail_update_preferences_non_existent_id,
                        'fail_update_preferences')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_preferences_no_data_package,
                      'fail_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(mock_program_dao)
        DUT.tree.get_node(1).data.pop('programinfo')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_preferences_no_data_package,
                        'fail_update_preferences')

    @pytest.mark.integration
    def test_do_update_data_manager_wrong_data_type(
            self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_preferences_wrong_data_type,
                      'fail_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(test_program_dao)

        _old = DUT.tree.get_node(1).data['programinfo'].hardware_active

        DUT.tree.get_node(1).data['programinfo'].hardware_active = {0: 1}
        DUT.do_update(1)

        pub.subscribe(self.on_fail_update_preferences_wrong_data_type,
                      'fail_update_preferences')

        DUT.tree.get_node(1).data['programinfo'].hardware_active = _old
