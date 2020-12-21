# type: ignore
# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Revision algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import MOCK_REVISIONS
from ramstk.controllers import dmRevision
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRevision


class MockDao:
    _all_revisions = []

    def do_delete(self, record):
        try:
            for _idx, _revision in enumerate(self._all_revisions):
                if _revision.revision_id == record.revision_id:
                    self._all_revisions.pop(_idx)
        except AttributeError:
            raise DataAccessError('')

    def do_insert(self, record):
        if record.revision_id != 0:
            self._all_revisions.append(record)
        elif record.revision_id == 0:
            raise DataAccessError('An error occured with RAMSTK.')

    def do_select_all(self, table, key, value, order=None,
                      _all=False):
        self._all_revisions = []
        for _key in MOCK_REVISIONS:
            _record = table()
            _record.revision_id = _key
            _record.set_attributes(MOCK_REVISIONS[_key])
            self._all_revisions.append(_record)

        return self._all_revisions

    def do_update(self, record):
        for _key in MOCK_REVISIONS:
            if _key == record.revision_id:
                MOCK_REVISIONS[_key]['name'] = str(record.name)
                MOCK_REVISIONS[_key]['cost'] = float(record.cost)

    def get_last_id(self, table, id_column):
        if table == 'ramstk_revision':
            _last_id = max(MOCK_REVISIONS.keys())
            if _last_id > 3:
                _last_id = -1
            return _last_id


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Revision data manager."""
        DUT = dmRevision()

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'revision'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all,
                                'request_retrieve_revisions')
        assert pub.isSubscribed(DUT.do_update, 'request_update_revision')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_revisions')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_revision_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_revision_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_revision_attributes')
        assert pub.isSubscribed(DUT._do_delete,
                                'request_delete_revision')
        assert pub.isSubscribed(DUT._do_insert_revision,
                                'request_insert_revision')

class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKRevision instances on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['revision'], RAMSTKRevision)

    @pytest.mark.unit
    def test_do_select_revision(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRevision on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')

        assert isinstance(_revision, RAMSTKRevision)
        assert _revision.availability_logistics == 0.9986
        assert _revision.name == 'Original Revision'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert DUT.do_select(100, table='revision') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_revision(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_revision topic was broadcast.")

    def on_fail_delete_revision(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent revision ID 300.')
        print("\033[35m\nfail_delete_revision topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_revision(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_revision,
                      'succeed_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_revision,
                        'succeed_delete_revision')

    @pytest.mark.unit
    def test_do_delete_revision_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent revision."""
        pub.subscribe(self.on_fail_delete_revision, 'fail_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_delete_revision', node_id=300)

        pub.unsubscribe(self.on_fail_delete_revision, 'fail_delete_revision')


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_revision_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Original Revision'
        assert attributes['program_time'] == 2562
        print("\033[36m\nsucceed_get_revision_attributes topic was broadcast")

    def on_succeed_get_revision_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['revision'], RAMSTKRevision)
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_revision(self, mock_program_dao):
        """_do_get_attributes() should return a dict of revision attributes on success."""
        pub.subscribe(self.on_succeed_get_revision_attrs,
                      'succeed_get_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_attributes(1, 'revision')

        pub.unsubscribe(self.on_succeed_get_revision_attrs,
                        'succeed_get_revision_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_set_revision_attributes',
                        node_id=[1,],
                        package={'revision_code': '-'})
        assert DUT.do_select(1, table='revision').revision_code == '-'

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_revision_tree,
                      'succeed_get_revision_tree')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_revision_tree,
                        'succeed_get_revision_tree')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_revision(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_revision topic was broadcast")

    def on_fail_insert_revision(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_revision topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_succeed_insert_revision,
                      'succeed_insert_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_insert_revision()

        assert isinstance(
            DUT.tree.get_node(3).data['revision'], RAMSTKRevision)
        assert DUT.tree.get_node(3).data['revision'].revision_id == 3
        assert DUT.tree.get_node(3).data['revision'].name == 'New Revision'

        pub.unsubscribe(self.on_succeed_insert_revision,
                        'succeed_insert_revision')

    @pytest.mark.unit
    def test_do_insert_database_error(self, mock_program_dao):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_fail_insert_revision,
                      'fail_insert_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_insert_revision()

        pub.unsubscribe(self.on_fail_insert_revision,
                        'fail_insert_revision')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_revision(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_fail_update_revision(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent revision with revision ID 100.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_revision_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for revision ID 1.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_revision,
                      'succeed_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')
        _revision.name = 'Test Revision'
        DUT.do_update(1)

        DUT.do_select_all()
        _revision = DUT.do_select(1, table='revision')

        assert _revision.name == 'Test Revision'

        pub.unsubscribe(self.on_succeed_update_revision,
                        'succeed_update_revision')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_revision, 'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_revision, 'fail_update_revision')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """ do_update() should raise the 'fail_update_validation' message when passed a Validation ID that doesn't exist in the tree. """
        pub.subscribe(self.on_fail_update_revision_no_data_package,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.tree.get_node(1).data['revision'].cost = None

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_revision_no_data_package,
                        'fail_update_revision')

    @pytest.mark.unit
    def test_do_update_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_revision_no_data_package,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        DUT.do_update(0)

        pub.unsubscribe(self.on_fail_update_revision_no_data_package,
                        'fail_update_revision')
