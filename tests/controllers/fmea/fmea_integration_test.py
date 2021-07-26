# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.fmea.fmea_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import (
    amFMEA,
    dmAction,
    dmCause,
    dmControl,
    dmFMEA,
    dmMechanism,
    dmMode,
)
from ramstk.models.programdb import (
    RAMSTKAction,
    RAMSTKCause,
    RAMSTKControl,
    RAMSTKMechanism,
    RAMSTKMode,
)


@pytest.fixture(scope="class")
def test_mode(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMode()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mode")
    pub.unsubscribe(dut._do_insert_mode, "request_insert_mode")

    # Delete the device under test.
    del dut


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
    pub.unsubscribe(dut.do_select_all, "selected_mode")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut._do_insert_mechanism, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_cause(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmCause()
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
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_cause")
    pub.unsubscribe(dut._do_insert_cause, "request_insert_cause")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_control(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmControl()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_control")
    pub.unsubscribe(dut.do_update, "request_update_control")
    pub.unsubscribe(dut.do_select_all, "selected_cause")
    pub.unsubscribe(dut.do_get_tree, "request_get_control_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_control")
    pub.unsubscribe(dut._do_insert_control, "request_insert_control")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_action(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmAction()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_cause")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_action")
    pub.unsubscribe(dut._do_insert_action, "request_insert_action")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="function")
def test_analysismanager(test_toml_user_configuration):
    """Get a analysis manager instance for each test function."""
    # Create the device under test (dut) and connect to the configuration.
    dut = amFMEA(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_tree, "succeed_retrieve_fmea")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_fmea_tree")
    pub.unsubscribe(dut._do_calculate_rpn, "request_calculate_rpn")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFMEA()
    dut.do_connect(test_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_insert, "succeed_insert_mode")
    pub.unsubscribe(dut.on_insert, "succeed_insert_mechanism")
    pub.unsubscribe(dut.on_insert, "succeed_insert_cause")
    pub.unsubscribe(dut.on_insert, "succeed_insert_control")
    pub.unsubscribe(dut.on_insert, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_mode_tree, "succeed_retrieve_modes")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_cause_tree, "succeed_retrieve_causes")
    pub.unsubscribe(dut.do_set_control_tree, "succeed_retrieve_controls")
    pub.unsubscribe(dut.do_set_action_tree, "succeed_retrieve_actions")
    pub.unsubscribe(dut.do_set_mode_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_cause_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_control_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_action_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_mode",
    "test_mechanism",
    "test_cause",
    "test_control",
    "test_action",
)
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_on_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("6").data["fmea"], RAMSTKMode)
        assert isinstance(tree.get_node("6.3").data["fmea"], RAMSTKMechanism)
        assert isinstance(tree.get_node("6.3.3").data["fmea"], RAMSTKCause)
        assert isinstance(tree.get_node("6.3.3.3c").data["fmea"], RAMSTKControl)
        assert isinstance(tree.get_node("6.3.3.3a").data["fmea"], RAMSTKAction)
        print("\033[36m\nsucceed_retrieve_fmea topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        test_datamanager,
        test_mode,
        test_mechanism,
        test_cause,
        test_control,
        test_action,
    ):
        """should return a records tree object."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmea")

        test_mode.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_cause.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_control.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_action.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert isinstance(test_datamanager.tree.get_node("6").data["fmea"], RAMSTKMode)
        assert isinstance(
            test_datamanager.tree.get_node("6.3").data["fmea"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3").data["fmea"], RAMSTKCause
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3c").data["fmea"], RAMSTKControl
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3a").data["fmea"], RAMSTKAction
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self,
        test_datamanager,
        test_mode,
        test_mechanism,
        test_cause,
        test_control,
        test_action,
    ):
        """should clear the records tree and repopulate the records tree."""

        test_mode.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_cause.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_control.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_action.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert isinstance(test_datamanager.tree.get_node("6").data["fmea"], RAMSTKMode)
        assert isinstance(
            test_datamanager.tree.get_node("6.3").data["fmea"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3").data["fmea"], RAMSTKCause
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3c").data["fmea"], RAMSTKControl
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3a").data["fmea"], RAMSTKAction
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmea")

        test_datamanager.on_select_all()

        assert isinstance(test_datamanager.tree.get_node("6").data["fmea"], RAMSTKMode)
        assert isinstance(
            test_datamanager.tree.get_node("6.3").data["fmea"], RAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3").data["fmea"], RAMSTKCause
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3c").data["fmea"], RAMSTKControl
        )
        assert isinstance(
            test_datamanager.tree.get_node("6.3.3.3a").data["fmea"], RAMSTKAction
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmea")


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_mode",
    "test_mechanism",
    "test_cause",
    "test_control",
    "test_action",
)
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_mode(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("7")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after inserting a "
            "Mode."
        )

    def on_succeed_insert_mechanism(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6.5")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after inserting a "
            "Mechanism."
        )

    def on_succeed_insert_cause(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.5")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after inserting a "
            "Cause."
        )

    def on_succeed_insert_control(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.3.5c")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after inserting a "
            "Control."
        )

    def on_succeed_insert_test_action(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.3.5a")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after inserting an "
            "Action."
        )

    @pytest.mark.integration
    def test_do_insert_mode(self, test_datamanager):
        """should add the new mode record to the records tree."""
        assert not test_datamanager.tree.contains("7")

        pub.subscribe(self.on_succeed_insert_mode, "succeed_retrieve_fmea")

        pub.sendMessage("request_insert_mode")

        assert test_datamanager.tree.contains("7")

        pub.unsubscribe(self.on_succeed_insert_mode, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_mechanism(self, test_datamanager):
        """should add the new mechanism record to the records tree."""
        assert not test_datamanager.tree.contains("6.5")

        pub.subscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_fmea")

        pub.sendMessage("request_insert_mechanism")

        assert test_datamanager.tree.contains("6.5")

        pub.unsubscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_cause(self, test_datamanager):
        """should add the new cause record to the records tree."""
        assert not test_datamanager.tree.contains("6.3.5")

        pub.subscribe(self.on_succeed_insert_cause, "succeed_retrieve_fmea")

        pub.sendMessage("request_insert_cause")

        assert test_datamanager.tree.contains("6.3.5")

        pub.unsubscribe(self.on_succeed_insert_cause, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_control(self, test_datamanager):
        """should add the new control record to the records tree."""
        assert not test_datamanager.tree.contains("6.3.3.5c")

        pub.subscribe(self.on_succeed_insert_control, "succeed_retrieve_fmea")

        pub.sendMessage("request_insert_control")

        assert test_datamanager.tree.contains("6.3.3.5c")

        pub.unsubscribe(self.on_succeed_insert_control, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_action(self, test_datamanager):
        """should add the new action record to the records tree."""
        assert not test_datamanager.tree.contains("6.3.3.5a")

        pub.subscribe(self.on_succeed_insert_test_action, "succeed_retrieve_fmea")

        pub.sendMessage("request_insert_action")

        assert test_datamanager.tree.contains("6.3.3.5a")

        pub.unsubscribe(self.on_succeed_insert_test_action, "succeed_retrieve_fmea")


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_mode",
    "test_mechanism",
    "test_cause",
    "test_control",
    "test_action",
)
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete_action(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("6.3.3.3a")
        assert tree.contains("6.3.3.3c")
        assert tree.contains("6.3.3")
        assert tree.contains("6.3")
        assert tree.contains("6")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after deleting "
            "an action."
        )

    def on_succeed_delete_control(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6")
        assert tree.contains("6.3")
        assert tree.contains("6.3.3")
        assert not tree.contains("6.3.3.4c")
        assert tree.contains("6.3.3.4a")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after deleting "
            "a control."
        )

    def on_succeed_delete_cause(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6")
        assert tree.contains("6.3")
        assert not tree.contains("6.3.3")
        assert not tree.contains("6.3.3.4c")
        assert not tree.contains("6.3.3.4a")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after deleting "
            "a cause."
        )

    def on_succeed_delete_mechanism(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("6")
        assert not tree.contains("6.3")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after deleting a "
            "mechanism."
        )

    def on_succeed_delete_mode(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("4")
        assert tree.contains("5")
        assert not tree.contains("6")
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast after deleting a "
            "mode."
        )

    @pytest.mark.integration
    def test_do_delete_action(self, test_datamanager):
        """should remove the deleted action record from the records tree."""
        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert test_datamanager.tree.contains("6.3.3")
        assert test_datamanager.tree.contains("6.3.3.3c")
        assert test_datamanager.tree.contains("6.3.3.4a")

        pub.subscribe(self.on_succeed_delete_action, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_action", node_id=3)

        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert test_datamanager.tree.contains("6.3.3")
        assert test_datamanager.tree.contains("6.3.3.3c")
        assert not test_datamanager.tree.contains("6.3.3.3a")
        assert test_datamanager.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_action, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_control(self, test_datamanager):
        """should remove the deleted control record from the records tree."""
        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert test_datamanager.tree.contains("6.3.3")
        assert test_datamanager.tree.contains("6.3.3.4c")
        assert test_datamanager.tree.contains("6.3.3.4a")

        pub.subscribe(self.on_succeed_delete_control, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_control", node_id=4)

        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert test_datamanager.tree.contains("6.3.3")
        assert not test_datamanager.tree.contains("6.3.3.4c")
        assert test_datamanager.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_control, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_cause(self, test_datamanager):
        """should remove the deleted cause record from the records tree."""
        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert test_datamanager.tree.contains("6.3.3")
        assert not test_datamanager.tree.contains("6.3.3.4c")
        assert test_datamanager.tree.contains("6.3.3.4a")

        pub.subscribe(self.on_succeed_delete_cause, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_cause", node_id=3)

        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")
        assert not test_datamanager.tree.contains("6.3.3")
        assert not test_datamanager.tree.contains("6.3.3.4c")
        assert not test_datamanager.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_cause, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_mechanism(self, test_datamanager):
        """should remove the deleted mechanism record from the records tree."""
        assert test_datamanager.tree.contains("6")
        assert test_datamanager.tree.contains("6.3")

        pub.subscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_mechanism", node_id=3)

        assert test_datamanager.tree.contains("6")
        assert not test_datamanager.tree.contains("6.3")

        pub.unsubscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_mode(self, test_datamanager):
        """should remove the deleted mode record from the records tree."""
        assert test_datamanager.tree.contains("6")

        pub.subscribe(self.on_succeed_delete_mode, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_mode", node_id=6)

        assert not test_datamanager.tree.contains("6")

        pub.unsubscribe(self.on_succeed_delete_mode, "succeed_retrieve_fmea")


@pytest.mark.usefixtures(
    "test_analysismanager",
    "test_datamanager",
    "test_mode",
    "test_mechanism",
    "test_cause",
    "test_control",
    "test_action",
)
class TestAnalysisMethods:
    """Class for FMEA analysis manager method tests."""

    def on_succeed_calculate_rpn_mechanism(self, tree: Tree):
        assert isinstance(tree, Tree)
        assert tree.get_node("6.3").data["fmea"].rpn == 240
        assert tree.get_node("6.3").data["fmea"].rpn_new == 45
        print(
            "\033[36m\nsucceed_calculate_rpn topic was broadcast after calculating "
            "mechanism RPN."
        )

    def on_succeed_calculate_rpn_cause(self, tree: Tree):
        assert isinstance(tree, Tree)
        assert tree.get_node("6.3").data["fmea"].rpn == 240
        assert tree.get_node("6.3").data["fmea"].rpn_new == 45
        print(
            "\033[36m\nsucceed_calculate_rpn topic was broadcast after calculating "
            "cause RPN."
        )

    @pytest.mark.integration
    def test_do_calculate_rpn_mechanism(self, test_analysismanager, test_datamanager):
        """should calculate the mechanism RPN."""
        pub.subscribe(self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_rpn")

        test_datamanager.on_select_all()

        test_analysismanager._tree.get_node("6").data["fmea"].rpn_severity = 5
        test_analysismanager._tree.get_node("6").data["fmea"].rpn_severity_new = 5
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_occurrence = 8
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_occurrence_new = 3
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_detection = 6
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_detection_new = 3

        pub.sendMessage("request_calculate_rpn")

        assert test_analysismanager._tree.get_node("6.3").data["fmea"].rpn == 240
        assert test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_new == 45

        pub.unsubscribe(
            self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_rpn"
        )

    @pytest.mark.skip
    def test_do_calculate_rpn_cause(self, test_analysismanager, test_datamanager):
        """should calculate the failure cause RPN."""
        pub.subscribe(self.on_succeed_calculate_rpn_cause, "succeed_calculate_rpn")

        test_datamanager.on_select_all()

        test_analysismanager._tree.get_node("6").data["fmea"].rpn_severity = 5
        test_analysismanager._tree.get_node("6").data["fmea"].rpn_severity_new = 5
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_occurrence = 8
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_occurrence_new = 3
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_detection = 6
        test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_detection_new = 3

        pub.sendMessage("request_calculate_rpn", method="cause")

        assert test_analysismanager._tree.get_node("6.3").data["fmea"].rpn == 240
        assert test_analysismanager._tree.get_node("6.3").data["fmea"].rpn_new == 45

        pub.unsubscribe(self.on_succeed_calculate_rpn_cause, "succeed_calculate_rpn")
