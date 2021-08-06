# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.pof.pof_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism, dmOpLoad, dmOpStress, dmPoF, dmTestMethod
from ramstk.models.programdb import (
    RAMSTKMechanism,
    RAMSTKOpLoad,
    RAMSTKOpStress,
    RAMSTKTestMethod,
)


@pytest.fixture(scope="class")
def test_mechanism(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMechanism()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opload(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpLoad()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opstress(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpStress()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "load_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_method(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmTestMethod()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "load_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_test_method")
    pub.unsubscribe(dut.do_insert, "request_insert_test_method")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmPoF()
    dut.do_connect(test_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_insert, "succeed_insert_mechanism")
    pub.unsubscribe(dut.on_insert, "succeed_insert_opload")
    pub.unsubscribe(dut.on_insert, "succeed_insert_opstress")
    pub.unsubscribe(dut.on_insert, "succeed_insert_test_method")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_opload_tree, "succeed_retrieve_oploads")
    pub.unsubscribe(dut.do_set_opstress_tree, "succeed_retrieve_opstresss")
    pub.unsubscribe(dut.do_set_test_method_tree, "succeed_retrieve_test_methods")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_opload_tree, "succeed_delete_opload")
    pub.unsubscribe(dut.do_set_opstress_tree, "succeed_delete_opstress")
    pub.unsubscribe(dut.do_set_test_method_tree, "succeed_delete_test_method")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_datamanager", "test_mechanism", "test_opload", "test_opstress", "test_method"
)
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_on_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("3").data["pof"], RAMSTKMechanism)
        assert isinstance(tree.get_node("3.3").data["pof"], RAMSTKOpLoad)
        assert isinstance(tree.get_node("3.3.3s").data["pof"], RAMSTKOpStress)
        assert isinstance(tree.get_node("3.3.3t").data["pof"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_retrieve_pof topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """on_select_all() should return a Tree() object populated with
        RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod instances
        on success."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "load_id": 3,
            }
        )
        test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "load_id": 3,
            }
        )

        assert isinstance(
            test_datamanager.tree.get_node("3").data["pof"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3").data["pof"], RAMSTKOpLoad
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3s").data["pof"], RAMSTKOpStress
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3t").data["pof"], RAMSTKTestMethod
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """on_select_all() should return a Tree() object populated with
        RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod instances
        on success."""
        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "load_id": 3,
            }
        )
        test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "load_id": 3,
            }
        )

        assert isinstance(
            test_datamanager.tree.get_node("3").data["pof"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3").data["pof"], RAMSTKOpLoad
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3s").data["pof"], RAMSTKOpStress
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3t").data["pof"], RAMSTKTestMethod
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

        test_datamanager.on_select_all()

        assert isinstance(
            test_datamanager.tree.get_node("3").data["pof"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3").data["pof"], RAMSTKOpLoad
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3s").data["pof"], RAMSTKOpStress
        )
        assert isinstance(
            test_datamanager.tree.get_node("3.3.3t").data["pof"], RAMSTKTestMethod
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """should return an empty records tree if the base tree is empty."""
        test_datamanager._mechanism_tree = Tree()

        assert test_datamanager.on_select_all() is None
        assert test_datamanager.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_datamanager", "test_mechanism", "test_opload", "test_opstress", "test_method"
)
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_mechanism(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("5")
        print("\033[36m\nsucceed_insert_mechanism topic was broadcast.")

    def on_succeed_insert_opload(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("5.5")
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    def on_succeed_insert_opstress(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("3.3.5s")
        print("\033[36m\nsucceed_insert_opstress topic was broadcast.")

    def on_succeed_insert_test_method(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("3.3.5t")
        print("\033[36m\nsucceed_insert_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_mechanism(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """_do_insert_opload() should send the success message after successfully
        inserting an operating load."""
        assert not test_datamanager.tree.contains("5")

        pub.subscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_mechanism",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            },
        )

        assert test_datamanager.tree.contains("5")

        pub.unsubscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_pof")

    @pytest.mark.skip
    def test_do_insert_opload(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """_do_insert_opload() should send the success message after successfully
        inserting an operating load."""
        assert not test_datamanager.tree.contains("5.5")

        pub.subscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_opload",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 5,
                "load_id": 5,
            },
        )

        assert test_datamanager.tree.contains("5.5")

        pub.unsubscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_opstress(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """_do_insert_opstress() should send the success message after successfully
        inserting an operating stress."""
        assert not test_datamanager.tree.contains("3.3.5s")

        pub.subscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_opstress",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 3,
                "load_id": 3,
                "stress_id": 4,
            },
        )

        assert test_datamanager.tree.contains("3.3.5s")

        pub.unsubscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_test_method(
        self, test_datamanager, test_mechanism, test_opload, test_opstress, test_method
    ):
        """_do_insert_testmethod() should send the success message after successfully
        inserting a test method."""
        assert not test_datamanager.tree.contains("3.3.5t")

        pub.subscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_test_method",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 3,
                "load_id": 3,
                "test_id": 4,
            },
        )

        assert test_datamanager.tree.contains("3.3.5t")

        pub.unsubscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")


@pytest.mark.usefixtures(
    "test_datamanager", "test_mechanism", "test_opload", "test_opstress", "test_method"
)
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete_test_method(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert tree.contains("3.3.3s")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\nsucceed_retrieve_pof topic was broadcast after deleting "
            "test method."
        )

    def on_succeed_delete_opstress(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\nsucceed_retrieve_pof topic was broadcast after deleting "
            "operating stress."
        )

    def on_succeed_delete_opload(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert not tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\nsucceed_retrieve_pof topic was broadcast after deleting "
            "operating load."
        )

    def on_succeed_delete_mechanism(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert not tree.contains("3.3")
        assert not tree.contains("3")
        print(
            "\033[36m\nsucceed_retrieve_pof topic was broadcast after deleting "
            "mechanism."
        )

    @pytest.mark.integration
    def test_do_delete_test_method(self, test_datamanager):
        """should remove the deleted test method record from the records tree."""
        assert test_datamanager.tree.contains("3")
        assert test_datamanager.tree.contains("3.3")
        assert test_datamanager.tree.contains("3.3.3s")
        assert test_datamanager.tree.contains("3.3.3t")
        assert test_datamanager.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_test_method, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_test_method", node_id=3)

        assert test_datamanager.tree.contains("3")
        assert test_datamanager.tree.contains("3.3")
        assert test_datamanager.tree.contains("3.3.3s")
        assert not test_datamanager.tree.contains("3.3.3t")
        assert test_datamanager.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_test_method, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_delete_opstress(self, test_datamanager):
        """should remove the deleted opstress record from the records tree."""
        assert test_datamanager.tree.contains("3")
        assert test_datamanager.tree.contains("3.3")
        assert test_datamanager.tree.contains("3.3.3s")
        assert test_datamanager.tree.contains("3.3.4s")
        assert test_datamanager.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_opstress, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_opstress", node_id=3)

        assert test_datamanager.tree.contains("3")
        assert test_datamanager.tree.contains("3.3")
        assert not test_datamanager.tree.contains("3.3.3s")
        assert test_datamanager.tree.contains("3.3.4s")
        assert test_datamanager.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_opstress, "succeed_retrieve_pof")

    @pytest.mark.skip
    def test_do_delete_opload(self, test_datamanager):
        """should remove the deleted opload record from the records tree."""
        assert test_datamanager.tree.contains("3")
        assert test_datamanager.tree.contains("3.3")
        assert test_datamanager.tree.contains("3.3.4s")
        assert test_datamanager.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_opload, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_opload", node_id=3)

        assert test_datamanager.tree.contains("3")
        assert not test_datamanager.tree.contains("3.3")
        assert not test_datamanager.tree.contains("3.3.4s")
        assert not test_datamanager.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_opload, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_delete_mechanism(self, test_datamanager):
        """should remove the deleted opload record from the records tree."""
        assert test_datamanager.tree.contains("3")

        pub.subscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_mechanism", node_id=3)

        assert not test_datamanager.tree.contains("3")

        pub.unsubscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_pof")
