# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Function algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_HAZARDS
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amHazards, dmHazards
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKHazardAnalysis


class MockDao:
    _all_hazards = []

    def do_delete(self, record):
        try:
            for _idx, _record in enumerate(self._all_hazards):
                if _record.hazard_id == record.hazard_id:
                    self._all_hazards.pop(_idx)
        except AttributeError:
            raise DataAccessError('')

    def do_insert(self, record):
        record.revision_id = 1
        if record.function_id < 10:
            self._all_hazards.append(record)
        else:
            raise DataAccessError('An error occured with RAMSTK.')

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        if table == RAMSTKHazardAnalysis:
            self._all_hazards = []
            _idx = 1
            for _key in MOCK_HAZARDS:
                _record = table()
                _record.revision_id = value[0]
                _record.function_id = value[1]
                _record.hazard_id = _idx
                _record.set_attributes(MOCK_HAZARDS[_key])
                self._all_hazards.append(_record)
                _idx += 1

        return self._all_hazards

    def do_update(self, record):
        for _key in MOCK_HAZARDS:
            if _key == record.hazard_id:
                MOCK_HAZARDS[_key][
                    'potential_hazard'] = record.potential_hazard

    def get_last_id(self, table, id_column):
        return max(MOCK_HAZARDS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Function data manager."""
        DUT = dmHazards()

        assert isinstance(DUT, dmHazards)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'hazards'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_function')
        assert pub.isSubscribed(DUT.do_update, 'request_update_hazard')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_hazards')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_hazard_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_hazard_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_hazard_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_hazard')
        assert pub.isSubscribed(DUT._do_insert_hazard, 'request_insert_hazard')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the function analysis
        manager."""
        DUT = amHazards(test_toml_user_configuration)

        assert isinstance(DUT, amHazards)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_hazard_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_hazard_tree')
        assert pub.isSubscribed(DUT.do_calculate_fha, 'request_calculate_fha')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_hazards(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_retrieve_hazards topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFunction instances on success."""
        pub.subscribe(self.on_succeed_retrieve_hazards,
                      'succeed_retrieve_hazards')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        pub.unsubscribe(self.on_succeed_retrieve_hazards,
                        'succeed_retrieve_hazards')

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Function ID is
        requested."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        assert DUT.do_select(100, table='hazard') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_hazard(self, node_id, tree):
        assert node_id == 1
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hazard topic was broadcast.")

    def on_fail_delete_hazard(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent hazard ID 10.')
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_hazard(self, mock_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is
        successfully deleted."""
        pub.subscribe(self.on_succeed_delete_hazard, 'succeed_delete_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_delete(1)

        assert DUT.tree.get_node(1) is None

        pub.unsubscribe(self.on_succeed_delete_hazard, 'succeed_delete_hazard')

    @pytest.mark.unit
    def test_do_delete_hazard_non_existent_id(self, mock_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is
        successfully deleted."""
        pub.subscribe(self.on_fail_delete_hazard, 'fail_delete_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_hazard, 'fail_delete_hazard')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_hazard(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_hazard(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.unit
    def test_insert_hazard(self, mock_program_dao):
        """_do_insert_hazard() should send the success message after
        successfully inserting a new hazard."""
        pub.subscribe(self.on_succeed_insert_hazard, 'succeed_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_insert_hazard(parent_id=1)

        assert isinstance(
            DUT.tree.get_node(2).data['hazard'], RAMSTKHazardAnalysis)

        pub.unsubscribe(self.on_succeed_insert_hazard, 'succeed_insert_hazard')

    @pytest.mark.unit
    def test_insert_hazard_no_function(self, mock_program_dao):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_hazard, 'fail_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_insert_hazard(parent_id=10)

        pub.unsubscribe(self.on_fail_insert_hazard, 'fail_insert_hazard')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_hazard_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_id'] == 1
        assert attributes['potential_hazard'] == ''
        print("\033[36m\nsucceed_get_hazards_attributes topic was broadcast.")

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['hazard_id'] == 1
        assert attributes['function_id'] == 1
        print(
            "\033[36m\nsucceed_get_all_hazard_attributes topic was broadcast")

    def on_succeed_get_hazard_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of failure definition
        records on success."""
        pub.subscribe(self.on_succeed_get_hazard_attrs,
                      'succeed_get_hazards_attributes')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_get_attributes(1, 'hazard')

        pub.unsubscribe(self.on_succeed_get_hazard_attrs,
                        'succeed_get_hazards_attributes')

    @pytest.mark.skip
    def test_do_get_all_attributes_data_manager(self, mock_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data
        tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_hazard_attributes')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs,
                        'succeed_get_all_hazard_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        pub.sendMessage('request_set_hazard_attributes',
                        node_id=[
                            1,
                        ],
                        package={'potential_hazard': 'Donald Trump'})
        assert DUT.do_select(1,
                             table='hazard').potential_hazard == 'Donald Trump'

    @pytest.mark.skip
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        pub.sendMessage('request_set_all_hazard_attributes',
                        attributes={
                            'hazard_id': 1,
                            'potential_cause': 'Apathy',
                            'potential_hazard': 'Donald Trump & family'
                        })
        assert DUT.do_select(1, table='hazard').potential_cause == 'Apathy'
        assert DUT.do_select(
            1, table='hazard').potential_hazard == 'Donald Trump & family'

        pub.sendMessage('request_set_all_hazard_attributes',
                        attributes={
                            'hazard_id': 1,
                            'potential_cause': '',
                            'potential_hazard': ''
                        })

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the hazard treelib Tree."""
        pub.subscribe(self.on_succeed_get_hazard_tree,
                      'succeed_get_hazard_tree')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_hazard_tree,
                        'succeed_get_hazard_tree')

    @pytest.mark.skip
    def test_get_all_attributes_analysis_manager(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hazard_attributes', node_id=1)

        assert isinstance(DUT._attributes, dict)
        assert DUT._attributes['revision_id'] == 1
        assert DUT._attributes['function_id'] == 1
        assert DUT._attributes['assembly_hri'] == 20

    @pytest.mark.unit
    def test_on_get_tree_analysis_manager(self, mock_program_dao,
                                          test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_function_tree message."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)
        DATAMGR.do_get_tree()

        assert isinstance(DUT._tree, Tree)
        assert isinstance(
            DUT._tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)


class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_hazard(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_hazard topic was broadcast")

    def on_fail_update_hazard(self, error_message):
        assert error_message == (
            'do_update: Attempted to delete non-existent hazard ID 100.')
        print("\033[35m\nfail_update_hazard topic was broadcast")

    def on_fail_update_hazard_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for hazard ID 1.')
        print("\033[35m\nfail_update_hazard topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_hazard, 'succeed_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.tree.get_node(1).data['hazard'].potential_hazard = 'Big Hazard'
        DUT.do_update(1)

        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        assert DUT.tree.get_node(
            1).data['hazard'].potential_hazard == 'Big Hazard'

        pub.unsubscribe(self.on_succeed_update_hazard, 'succeed_update_hazard')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_hazard, 'fail_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_hazard, 'fail_update_hazard')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_hazard_no_data, 'fail_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.tree.get_node(1).data = None

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_hazard_no_data,
                        'fail_update_hazard')

    @pytest.mark.unit
    def test_do_update_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.do_update(0)


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_hri(self, mock_program_dao,
                              test_toml_user_configuration):
        """do_calculate_hri() should calculate the hazard risk index hazard
        analysis."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)

        _hazard = DATAMGR.do_select(1, 'hazard')
        _hazard.assembly_severity = 'Major'
        _hazard.assembly_probability = 'Level A - Frequent'
        _hazard.system_severity = 'Medium'
        _hazard.system_probability = 'Level A - Frequent'
        _hazard.assembly_severity_f = 'Medium'
        _hazard.assembly_probability_f = 'Level B - Reasonably Probable'
        _hazard.system_severity_f = 'Medium'
        _hazard.system_probability_f = 'Level C - Occasional'
        DATAMGR.do_update(1)
        pub.sendMessage('request_get_hazard_attributes',
                        node_id=1,
                        table='hazard')

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['assembly_hri'] == 30
        assert DUT._attributes['system_hri'] == 20
        assert DUT._attributes['assembly_hri_f'] == 16
        assert DUT._attributes['system_hri_f'] == 12

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, mock_program_dao,
                                       test_toml_user_configuration):
        """do_calculate_user_defined() should calculate the user-defined hazard
        analysis."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)

        _hazard = DATAMGR.do_select(1, 'hazard')
        _hazard.user_float_1 = 1.5
        _hazard.user_float_2 = 0.8
        _hazard.user_int_1 = 2
        _hazard.function_1 = 'uf1*uf2'
        _hazard.function_2 = 'res1/ui1'
        DATAMGR.do_update(1)
        pub.sendMessage('request_get_hazard_attributes',
                        node_id=1,
                        table='hazard')

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['result_1'] == pytest.approx(1.2)
        assert DUT._attributes['result_2'] == pytest.approx(0.6)
