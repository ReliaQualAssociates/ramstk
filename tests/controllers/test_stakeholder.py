# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import MOCK_STAKEHOLDERS
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amStakeholder, dmStakeholder
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKStakeholder


class MockDao:
    _all = []

    def do_delete(self, item):
        for _idx, _requirement in enumerate(self._all):
            try:
                if _requirement.requirement_id == item.requirement_id:
                    self._all.pop(_idx)
            except AttributeError:
                raise DataAccessError('')

    def do_insert(self, record):
        if record.stakeholder_id not in MOCK_STAKEHOLDERS.keys():
            self._all.append(record)
        else:
            raise DataAccessError(msg = (
                "There was an database error when attempting to add a "
                "record."))

    def do_select_all(self, table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        self._all = []
        for _key in MOCK_STAKEHOLDERS:
            _record = table()
            _record.revision_id = value
            _record.stakeholder_id = _key
            _record.set_attributes(MOCK_STAKEHOLDERS[_key])
            self._all.append(_record)

        return self._all

    def do_update(self, record):
        for _key in MOCK_STAKEHOLDERS:
            if _key == record.stakeholder_id:
                MOCK_STAKEHOLDERS[_key]['customer_rank'] = record.customer_rank
                MOCK_STAKEHOLDERS[_key]['description'] = record.description
                MOCK_STAKEHOLDERS[_key]['group'] = record.group
                MOCK_STAKEHOLDERS[_key]['improvement'] = record.improvement
                MOCK_STAKEHOLDERS[_key]['overall_weight'] = \
                    record.overall_weight
                MOCK_STAKEHOLDERS[_key]['planned_rank'] = record.planned_rank
                MOCK_STAKEHOLDERS[_key]['priority'] = record.priority
                MOCK_STAKEHOLDERS[_key]['requirement_id'] = \
                    record.requirement_id
                MOCK_STAKEHOLDERS[_key]['stakeholder'] = record.stakeholder
                MOCK_STAKEHOLDERS[_key]['user_float_1'] = record.user_float_1
                MOCK_STAKEHOLDERS[_key]['user_float_2'] = record.user_float_2
                MOCK_STAKEHOLDERS[_key]['user_float_3'] = record.user_float_3
                MOCK_STAKEHOLDERS[_key]['user_float_4'] = record.user_float_4
                MOCK_STAKEHOLDERS[_key]['user_float_5'] = record.user_float_5


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Stakeholder data manager."""
        DUT = dmStakeholder()

        assert isinstance(DUT, dmStakeholder)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'stakeholder'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT._do_delete_stakeholder,
                                'request_delete_stakeholder')
        assert pub.isSubscribed(DUT.do_insert_stakeholder,
                                'request_insert_stakeholder')
        assert pub.isSubscribed(DUT.do_update_stakeholder,
                                'request_update_stakeholder')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_stakeholders')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_stakeholder_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                                'request_get_all_stakeholder_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_stakeholder_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_stakeholder_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'request_set_all_stakeholder_attributes')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the function analysis manager."""
        DUT = amStakeholder(test_toml_user_configuration)

        assert isinstance(DUT, amStakeholder)
        assert isinstance(DUT.RAMSTK_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_stakeholder_attributes')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_get_stakeholder_tree')
        assert pub.isSubscribed(DUT.do_calculate_stakeholder,
                                'request_calculate_stakeholder')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_stakeholders(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_retrieve_stakeholders topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all(1) should return a Tree() object populated with RAMSTKStakeholder instances on success."""
        pub.subscribe(self.on_succeed_retrieve_stakeholders,
                      'succeed_retrieve_stakeholders')
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.tree.get_node(1).data, dict)
        assert isinstance(
            DUT.tree.get_node(1).data['stakeholder'], RAMSTKStakeholder)

        pub.unsubscribe(self.on_succeed_retrieve_stakeholders,
                        'succeed_retrieve_stakeholders')

    @pytest.mark.unit
    def test_do_select_stakeholder(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKStakeholder on success."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _stakeholder = DUT.do_select(1, table='stakeholder')

        assert isinstance(_stakeholder, RAMSTKStakeholder)
        assert _stakeholder.description == 'Stakeholder Input'
        assert _stakeholder.priority == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Stakeholder ID is requested."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='stakeholder') is None


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_stakeholder(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_stakeholder topic was broadcast.")

    def on_fail_delete_stakeholder(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent stakeholder ID '
            '300.')
        print("\033[35m\nfail_delete_stakeholder topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_stakeholder(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_stakeholder,
                      'succeed_delete_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete_stakeholder(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_stakeholder,
                        'succeed_delete_stakeholder')

    @pytest.mark.unit
    def test_do_delete_stakeholder_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent stakeholder."""
        pub.subscribe(self.on_fail_delete_stakeholder,
                      'fail_delete_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete_stakeholder(300)

        pub.unsubscribe(self.on_fail_delete_stakeholder,
                        'fail_delete_stakeholder')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_stakeholder_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['stakeholder_id'] == 1
        assert attributes['description'] == 'Stakeholder Input'
        assert attributes['priority'] == 1
        print(
            "\033[36m\nsucceed_get_stakeholder_attributes topic was broadcast")

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['stakeholder_id'] == 1
        assert attributes['description'] == 'Stakeholder Input'
        assert attributes['priority'] == 1
        print(
            "\033[36m\nsucceed_get_all_stakeholder_attributes topic was broadcast"
        )

    def on_succeed_get_stakeholder_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(dmtree.get_node(1).data, dict)
        assert isinstance(
            dmtree.get_node(1).data['stakeholder'], RAMSTKStakeholder)
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_stakeholder(self, mock_program_dao):
        """do_get_attributes() should return a dict of stakeholder attributes on success."""
        pub.subscribe(self.on_succeed_get_stakeholder_attrs,
                      'succeed_get_stakeholder_attributes')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'stakeholder')

        pub.unsubscribe(self.on_succeed_get_stakeholder_attrs,
                        'succeed_get_stakeholder_attributes')

    @pytest.mark.unit
    def test_do_get_all_attributes_data_manager(self, mock_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_stakeholder_attributes')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs,
                        'succeed_get_all_stakeholder_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_stakeholder_attributes',
                        node_id=[1, -1],
                        package={'stakeholder': 'Customer'})
        assert DUT.do_select(1, table='stakeholder').stakeholder == 'Customer'

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_stakeholder_attributes',
                        attributes={
                            'stakeholder_id': 1,
                            'stakeholder': 'Service',
                            'description':
                            'This is a description added by a test.',
                            'priority': 2
                        })
        assert DUT.do_select(1, table='stakeholder').stakeholder == 'Service'
        assert DUT.do_select(
            1, table='stakeholder'
        ).description == 'This is a description added by a test.'
        assert DUT.do_select(1, table='stakeholder').priority == 2

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the stakeholder treelib Tree."""
        pub.subscribe(self.on_succeed_get_stakeholder_tree,
                      'succeed_get_stakeholder_tree')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_stakeholder_tree,
                        'succeed_get_stakeholder_tree')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_stakeholder(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_stakeholder topic was broadcast")

    def on_fail_insert_stakeholder(self, error_message):
        assert error_message == 'There was an database error when attempting to add a record.'
        print("\033[35m\nfail_insert_stakeholder topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_stakeholder(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new top-level stakeholder."""
        pub.subscribe(self.on_succeed_insert_stakeholder,
                      'succeed_insert_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_insert_stakeholder()

        assert isinstance(
            DUT.tree.get_node(3).data['stakeholder'], RAMSTKStakeholder)
        assert DUT.tree.get_node(3).data['stakeholder'].stakeholder_id == 3
        assert DUT.tree.get_node(
            3).data['stakeholder'].description == 'New Stakeholder Input'

        pub.unsubscribe(self.on_succeed_insert_stakeholder,
                        'succeed_insert_stakeholder')

    @pytest.mark.unit
    def test_do_insert_stakeholder_existing_id(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new top-level stakeholder."""
        pub.subscribe(self.on_fail_insert_stakeholder,
                      'fail_insert_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.last_id = DUT.last_id - 1

        DUT.do_insert_stakeholder()

        pub.unsubscribe(self.on_fail_insert_stakeholder,
                        'fail_insert_stakeholder')

@pytest.mark.usefixtures('test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_stakeholder(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_stakeholder topic was broadcast")

    def on_fail_update_stakeholder(self, error_message):
        assert error_message == (
            'Attempted to save non-existent stakeholder with stakeholder ID 100.'
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_stakeholder_no_package(self, error_message):
        assert error_message == (
            'No data package found for stakeholder ID 1.'
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_stakeholder,
                      'succeed_update_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _stakeholder = DUT.do_select(1, table='stakeholder')
        _stakeholder.description = 'Test Stakeholder'
        DUT.do_update_stakeholder(1)

        DUT.do_select_all(attributes={'revision_id': 1})
        _stakeholder = DUT.do_select(1, table='stakeholder')

        assert _stakeholder.description == 'Test Stakeholder'

        pub.unsubscribe(self.on_succeed_update_stakeholder,
                        'succeed_update_stakeholder')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Stakeholder ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_stakeholder,
                      'fail_update_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update_stakeholder(100)

        pub.unsubscribe(self.on_fail_update_stakeholder,
                        'fail_update_stakeholder')

    @pytest.mark.unit
    def test_do_update_node_zero(self, mock_program_dao):
        """ do_update() should return None when passed Validation ID=0. """
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_update_stakeholder(0) is None

    @pytest.mark.unit
    def test_do_update_data_manager_no_data_package(self, mock_program_dao):
        """ do_update() should send the fail_update_requirement message when there is no data package attached to the node. """
        pub.subscribe(self.on_fail_update_stakeholder_no_package,
                      'fail_update_requirement')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('stakeholder')
        DUT.do_update_stakeholder(1)

        pub.unsubscribe(self.on_fail_update_stakeholder_no_package,
                        'fail_update_requirement')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_improvement(self, mock_program_dao,
                                      test_toml_user_configuration):
        """do_calculate_stakeholder() should calculate the improvement factor and overall weight of a stakeholder input."""
        DATAMGR = dmStakeholder()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amStakeholder(test_toml_user_configuration)

        pub.sendMessage('request_get_stakeholder_tree')

        _stakeholder = DATAMGR.do_select(1, 'stakeholder')
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        DATAMGR.do_update_stakeholder(1)

        pub.sendMessage('request_calculate_stakeholder', node_id=1)

        assert DUT._attributes['improvement'] == 1.2
        assert DUT._attributes['overall_weight'] == 12.48
