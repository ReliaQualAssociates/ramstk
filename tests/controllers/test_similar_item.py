# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_similar_item.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_SIMILAR_ITEM
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amSimilarItem, dmSimilarItem
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKSimilarItem


class MockDao:
    _all_similar_item = []

    def do_delete(self, record):
        if record is None:
            raise DataAccessError('')
        else:
            for _idx, _record in enumerate(self._all_similar_item):
                if _record.hardware_id == record.hardware_id:
                    self._all_similar_item.pop(_idx)

    def do_insert(self, record):
        if record.hardware_id == 5:
            raise DataAccessError('An error occurred with RAMSTK.')
        elif record == RAMSTKSimilarItem:
            self._all_similar_item.append(record)

    def do_insert_many(self, records):
        for _record in records:
            self.do_insert(_record)

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        if table == RAMSTKSimilarItem:
            self._all_similar_item = []
            for _key in MOCK_SIMILAR_ITEM:
                _record = table()
                _record.revision_id = value
                _record.hardware_id = _key
                _record.set_attributes(MOCK_SIMILAR_ITEM[_key])
                self._all_similar_item.append(_record)

        return self._all_similar_item

    def do_update(self, record):
        for _key in MOCK_SIMILAR_ITEM:
            if _key == record.hardware_id:
                MOCK_SIMILAR_ITEM[_key]['change_factor_1'] = float(
                    record.change_factor_1)
                MOCK_SIMILAR_ITEM[_key]['change_factor_2'] = float(
                    record.change_factor_2)
                MOCK_SIMILAR_ITEM[_key]['change_factor_3'] = float(
                    record.change_factor_3)


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Hardware data manager."""
        DUT = dmSimilarItem()

        assert isinstance(DUT, dmSimilarItem)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'similar_items'
        assert DUT._root == 0
        assert DUT._pkey == {'similar_item': ['revision_id', 'hardware_id']}
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_similar_item_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_similar_item_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'wvw_editing_similar_item')
        assert pub.isSubscribed(DUT.do_set_tree,
                                'succeed_calculate_similar_item')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_similar_items')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_similar_item_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_similar_item')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_hardware')
        assert pub.isSubscribed(DUT._do_insert_similar_item,
                                'request_insert_similar_item')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the hardware analysis
        manager."""
        DUT = amSimilarItem(test_toml_user_configuration)

        assert isinstance(DUT, amSimilarItem)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert DUT._node_hazard_rate == 0.0
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_similar_item_attributes')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_get_similar_item_tree')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_retrieve_similar_item')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_update_similar_item')
        assert pub.isSubscribed(DUT._do_calculate_similar_item,
                                'request_calculate_similar_item')
        assert pub.isSubscribed(DUT._do_roll_up_change_descriptions,
                                'request_roll_up_change_descriptions')
        assert pub.isSubscribed(DUT._on_get_hardware_attributes,
                                'succeed_get_all_hardware_attributes')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['similar_item'], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_retrieve_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKHardware instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_similar_item')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing allocation
        tree."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_similar_item')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKSimilarItem on
        success."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _similar_item = DUT.do_select(1, table='similar_item')

        assert isinstance(_similar_item, RAMSTKSimilarItem)
        assert _similar_item.change_description_1 == ''
        assert _similar_item.temperature_from == 30.0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Hardware ID is
        requested."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='hardware') is None


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_similar_item(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_similar_item topic was broadcast.")

    def on_fail_delete_similar_item_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent similar item "
            "record with hardware ID 300.")
        print("\033[35m\nfail_delete_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_similar_item,
                      'succeed_delete_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete_similar_item,
                        'succeed_delete_similar_item')

    @pytest.mark.unit
    def test_do_delete_with_children(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_similar_item,
                      'succeed_delete_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=2)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_similar_item,
                        'succeed_delete_similar_item')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_similar_item_non_existent_id,
                      'fail_delete_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=300)

        pub.unsubscribe(self.on_fail_delete_similar_item_non_existent_id,
                        'fail_delete_similar_item')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['change_description_1'] == ''
        assert attributes['change_description_2'] == ''
        assert attributes['change_description_3'] == ''
        assert attributes['change_description_4'] == ''
        assert attributes['change_description_5'] == ''
        assert attributes['change_description_6'] == ''
        assert attributes['change_description_7'] == ''
        assert attributes['change_description_8'] == ''
        assert attributes['change_description_9'] == ''
        assert attributes['change_description_10'] == ''
        assert attributes['change_factor_1'] == 1.0
        assert attributes['change_factor_2'] == 1.0
        assert attributes['change_factor_3'] == 1.0
        assert attributes['change_factor_4'] == 1.0
        assert attributes['change_factor_5'] == 1.0
        assert attributes['change_factor_6'] == 1.0
        assert attributes['change_factor_7'] == 1.0
        assert attributes['change_factor_8'] == 1.0
        assert attributes['change_factor_9'] == 1.0
        assert attributes['change_factor_10'] == 1.0
        assert attributes['environment_from_id'] == 0
        assert attributes['environment_to_id'] == 0
        assert attributes['function_1'] == '0'
        assert attributes['function_2'] == '0'
        assert attributes['function_3'] == '0'
        assert attributes['function_4'] == '0'
        assert attributes['function_5'] == '0'
        assert attributes['parent_id'] == 1
        assert attributes['similar_item_method_id'] == 1
        assert attributes['quality_from_id'] == 0
        assert attributes['quality_to_id'] == 0
        assert attributes['result_1'] == 0.0
        assert attributes['result_2'] == 0.0
        assert attributes['result_3'] == 0.0
        assert attributes['result_4'] == 0.0
        assert attributes['result_5'] == 0.0
        assert attributes['temperature_from'] == 30.0
        assert attributes['temperature_to'] == 30.0
        assert attributes['user_blob_1'] == ''
        assert attributes['user_blob_2'] == ''
        assert attributes['user_blob_3'] == ''
        assert attributes['user_blob_4'] == ''
        assert attributes['user_blob_5'] == ''
        assert attributes['user_float_1'] == 0.0
        assert attributes['user_float_2'] == 0.0
        assert attributes['user_float_3'] == 0.0
        assert attributes['user_float_4'] == 0.0
        assert attributes['user_float_5'] == 0.0
        assert attributes['user_int_1'] == 0
        assert attributes['user_int_2'] == 0
        assert attributes['user_int_3'] == 0
        assert attributes['user_int_4'] == 0
        assert attributes['user_int_5'] == 0
        print("\033[36m\nsucceed_get_similar_item_attributes topic was "
              "broadcast.")

    def on_succeed_get_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['similar_item'], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_get_similar_item_tree topic was broadcast.")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of hardware attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_similar_item_attributes')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage(
            'request_get_similar_item_attributes',
            node_id=2,
            table='similar_item',
        )

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_similar_item_attributes')

    @pytest.mark.unit
    def test_get_all_attributes_analysis_manager(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amSimilarItem(test_toml_user_configuration)

        pub.sendMessage('request_get_similar_item_attributes',
                        node_id=2,
                        table='similar_item')

        assert DUT._attributes['hardware_id'] == 2
        assert DUT._attributes['change_description_1'] == ''
        assert DUT._attributes['change_description_2'] == ''
        assert DUT._attributes['change_factor_1'] == 1.0
        assert DUT._attributes['change_factor_1'] == 1.0

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao, test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_hardware_tree message."""
        pub.subscribe(self.on_succeed_get_tree,
                      'succeed_get_similar_item_tree')

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_get_similar_item_tree')

        pub.unsubscribe(self.on_succeed_get_tree,
                        'succeed_get_similar_item_tree')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_similar_item_attributes',
                        node_id=[2, -1],
                        package={
                            'change_description_1':
                            'Testing set name from moduleview.'
                        })
        assert DUT.do_select(
            2, table='similar_item'
        ).change_description_1 == 'Testing set name from moduleview.'

        pub.sendMessage('request_set_similar_item_attributes',
                        node_id=[2, -1],
                        package={'change_factor_1': 0.003862})
        assert DUT.do_select(2,
                             table='similar_item').change_factor_1 == 0.003862


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_similar_item(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(node_id).data['similar_item'], RAMSTKSimilarItem)
        assert tree.get_node(node_id).data['similar_item'].revision_id == 1
        assert tree.get_node(node_id).data['similar_item'].hardware_id == 4
        assert tree.get_node(node_id).data['similar_item'].parent_id == 1
        print("\033[36m\nsucceed_insert_similar_item topic was broadcast.")

    def on_fail_insert_similar_item_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new sibling hardware assembly."""
        pub.subscribe(self.on_succeed_insert_similar_item,
                      'succeed_insert_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_insert_similar_item',
                        hardware_id=4,
                        parent_id=1)

        pub.unsubscribe(self.on_succeed_insert_similar_item,
                        'succeed_insert_similar_item')

    @pytest.mark.unit
    def test_do_insert_similar_item_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_similar_item_db_error,
                      'fail_insert_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_similar_item(hardware_id=5, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_similar_item_db_error,
                        'fail_insert_similar_item')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_similar_item(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data['similar_item'].parent_id == 1
        assert tree.get_node(
            2).data['similar_item'].percent_weight_factor == 0.9832
        assert tree.get_node(2).data['similar_item'].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_similar_item topic was broadcast.")

    def on_fail_update_similar_item_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent similar item record '
            'ID 100.')
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_similar_item_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'similar item record ID 1.')
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_similar_item_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for similar item '
            'record ID 1 was the wrong type.')
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_similar_item,
                      'succeed_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_update_similar_item', node_id=2)

        pub.unsubscribe(self.on_succeed_update_similar_item,
                        'succeed_update_similar_item')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_similar_item_non_existent_id,
                      'fail_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_similar_item_non_existent_id,
                        'fail_update_similar_item')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_similar_item_no_data,
                      'fail_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('similar_item')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_similar_item_no_data,
                        'fail_update_similar_item')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_similar_item_wrong_data_type,
                      'fail_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _similar_item = DUT.do_select(1, table='similar_item')
        _similar_item.change_factor_1 = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_similar_item_wrong_data_type,
                        'fail_update_similar_item')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _similar_item = DUT.do_select(1, table='similar_item')
        _similar_item.change_factor_1 = {1: 2}

        DUT.do_update(0)

    @pytest.mark.unit
    def test_do_update_all(self, mock_program_dao):
        """do_update_all() should return a zero error code on success."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(tree):
            assert isinstance(tree, Tree)

        pub.subscribe(on_message, 'succeed_update_similar_item')

        pub.sendMessage('request_update_all_similar_items')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for similar item methods test suite."""
    def on_succeed_roll_up(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['similar_item'].change_description_1 == (
            'This is change description 1 for assembly 2.\n\n')
        assert tree.get_node(1).data['similar_item'].change_description_2 == (
            'This is change description 2 for assembly 2.\n\n')
        assert tree.get_node(1).data['similar_item'].change_description_3 == (
            'This is change description 3 for assembly 2.\n\n')
        print(
            "\033[36m\nsucceed_roll_up_change_descriptions topic was broadcast."
        )

    @pytest.mark.unit
    def test_do_calculate_topic_633(self, mock_program_dao,
                                    test_toml_user_configuration):
        """do_calculate_goal() should calculate the Topic 6.3.3 similar
        item."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._node_hazard_rate = 0.000628
        DUT._system_hazard_rate = 0.002681

        DUT._tree.get_node(1).data['similar_item'].similar_item_method_id = 1
        DUT._tree.get_node(1).data['similar_item'].change_description_1 = (
            'Test change description for factor #1.')
        DUT._tree.get_node(1).data['similar_item'].environment_from_id = 2
        DUT._tree.get_node(1).data['similar_item'].environment_to_id = 3
        DUT._tree.get_node(1).data['similar_item'].quality_from_id = 1
        DUT._tree.get_node(1).data['similar_item'].quality_to_id = 2
        DUT._tree.get_node(1).data['similar_item'].temperature_from = 55.0
        DUT._tree.get_node(1).data['similar_item'].temperature_to = 65.0

        pub.sendMessage('request_calculate_similar_item', node_id=1)

        assert DUT._tree.get_node(
            1).data['similar_item'].change_factor_1 == 0.8
        assert DUT._tree.get_node(
            1).data['similar_item'].change_factor_2 == 1.4
        assert DUT._tree.get_node(
            1).data['similar_item'].change_factor_3 == 1.0
        assert DUT._tree.get_node(
            1).data['similar_item'].result_1 == pytest.approx(0.0005607143)

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, mock_program_dao,
                                       test_toml_user_configuration):
        """do_calculate_goal() should calculate the Topic 644 similar item."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._node_hazard_rate = 0.00617
        DUT._system_hazard_rate = 0.00617

        DUT._tree.get_node(1).data['similar_item'].similar_item_method_id = 2
        DUT._tree.get_node(1).data['similar_item'].change_description_1 = (
            'Test change description for '
            'factor #1.')
        DUT._tree.get_node(1).data['similar_item'].change_factor_1 = 0.85
        DUT._tree.get_node(1).data['similar_item'].change_factor_2 = 1.2
        DUT._tree.get_node(1).data['similar_item'].function_1 = 'pi1*pi2*hr'
        DUT._tree.get_node(1).data['similar_item'].function_2 = '0'
        DUT._tree.get_node(1).data['similar_item'].function_3 = '0'
        DUT._tree.get_node(1).data['similar_item'].function_4 = '0'
        DUT._tree.get_node(1).data['similar_item'].function_5 = '0'

        pub.sendMessage('request_calculate_similar_item', node_id=1)

        assert DUT._tree.get_node(
            1).data['similar_item'].change_description_1 == (
                'Test change description for factor #1.')
        assert DUT._tree.get_node(
            1).data['similar_item'].change_factor_1 == 0.85
        assert DUT._tree.get_node(
            1).data['similar_item'].change_factor_2 == 1.2
        assert DUT._tree.get_node(
            1).data['similar_item'].result_1 == pytest.approx(0.0062934)

    @pytest.mark.unit
    def test_do_roll_up_change_descriptions(self, mock_program_dao,
                                            test_toml_user_configuration):
        """do_roll_up_change_descriptions() should combine all child change
        descriptions into a single change description for the parent."""
        pub.subscribe(self.on_succeed_roll_up,
                      'succeed_roll_up_change_descriptions')

        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'hardware_id': 1})

        DUT._tree.get_node(2).data['similar_item'].change_description_1 = (
            'This is change description 1 for assembly 2.')
        DUT._tree.get_node(2).data['similar_item'].change_description_2 = (
            'This is change description 2 for assembly 2.')
        DUT._tree.get_node(2).data['similar_item'].change_description_3 = (
            'This is change description 3 for assembly 2.')

        pub.sendMessage('request_roll_up_change_descriptions',
                        node=DUT._tree.get_node(1))

        pub.unsubscribe(self.on_succeed_roll_up,
                        'succeed_roll_up_change_descriptions')

    @pytest.mark.unit
    def test_on_select_hardware(self, mock_program_dao,
                                test_toml_user_configuration):
        """_on_select_hardware() should assign the node hazard rate to the
        _node_hazard_rate attribute."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'hardware_id': 1})

        pub.sendMessage('succeed_get_all_hardware_attributes',
                        attributes={
                            'hardware_id': 1,
                            'hazard_rate_active': 0.00032,
                            'hardware_id': 2
                        })

        assert DUT._node_hazard_rate == 0.00032
