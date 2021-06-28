# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opload.opload_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Load algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKOpLoad
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpLoad
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKOpLoad


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opload_1 = MockRAMSTKOpLoad()
    _opload_1.revision_id = 1
    _opload_1.hardware_id = 1
    _opload_1.mode_id = 6
    _opload_1.mechanism_id = 2
    _opload_1.load_id = 1
    _opload_1.damage_model = ""
    _opload_1.description = "Test Operating Load #1"
    _opload_1.priority_id = 0

    _opload_2 = MockRAMSTKOpLoad()
    _opload_2.revision_id = 1
    _opload_2.hardware_id = 1
    _opload_2.mode_id = 6
    _opload_2.mechanism_id = 2
    _opload_2.load_id = 2
    _opload_2.damage_model = ""
    _opload_2.description = "Test Operating Load #2"
    _opload_2.priority_id = 0

    DAO = MockDAO()
    DAO.table = [
        _opload_1,
        _opload_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpLoad()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_opload")
    pub.unsubscribe(dut._do_insert_opload, "request_insert_opload")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmOpLoad()

        assert isinstance(DUT, dmOpLoad)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "oploads"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_mechanism")
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_opload_attributes")
        assert pub.isSubscribed(DUT.do_set_attributes, "request_set_opload_attributes")
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_opload")
        assert pub.isSubscribed(DUT.do_update, "request_update_opload")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_opload_tree")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_opload")
        assert pub.isSubscribed(DUT._do_insert_opload, "request_insert_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["opload"], MockRAMSTKOpLoad)
        print("\033[36m\nsucceed_retrieve_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoad instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoad instances on success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKOpLoad on
        success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        _opload = test_datamanager.do_select(2, table="opload")

        assert isinstance(_opload, MockRAMSTKOpLoad)
        assert _opload.description == "Test Operating Load #2"
        assert _opload.priority_id == 0

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent opload ID is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        assert test_datamanager.do_select(100, table="opload") is None


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_opload topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent OpLoad ID 300."
        )
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent OpLoad ID 2."
        )
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager._do_delete(2)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_opload")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager.tree.remove_node(2)
        test_datamanager._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["load_id"] == 1
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(2).data["opload"], MockRAMSTKOpLoad)
        print("\033[36m\nsucceed_get_opload_tree topic was broadcast")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager.do_get_attributes(1, "opload")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        test_datamanager.do_set_attributes(node_id=[1, -1], package={"priority_id": 4})
        test_datamanager.do_set_attributes(
            node_id=[1, -1], package={"description": "Big test operating load."}
        )

        pub.unsubscribe(
            test_datamanager.do_set_attributes, "request_set_opload_attributes"
        )

        assert (
            test_datamanager.do_select(1, table="opload").description
            == "Big test operating load."
        )
        assert test_datamanager.do_select(1, table="opload").priority_id == 4

    @pytest.mark.pof
    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, test_datamanager):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["opload"], RAMSTKOpLoad)
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager._do_insert_opload(2)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent opload with opload ID 100."
        )
        print("\033[35m\nfail_update_opload topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for opload ID 2.")
        print("\033[35m\nfail_update_opload topic was broadcast")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a PoF ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager.do_update(100, table="opload")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager.tree.get_node(2).data.pop("opload")
        test_datamanager.do_update(2, table="opload")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_opload")
