# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.fmea.fmea_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKActionRecord,
    RAMSTKCauseRecord,
    RAMSTKControlRecord,
    RAMSTKMechanismRecord,
    RAMSTKModeRecord,
)
from ramstk.models.dbviews import RAMSTKFMEAView

TEST_IDS = {
    "mode": "6",
    "mechanism": "6.3",
    "cause": "6.3.3",
    "control": "6.3.3.3c",
    "action": "6.3.3.3a",
}


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mode_table_model",
    "test_mechanism_table_model",
    "test_cause_table_model",
    "test_control_table_model",
    "test_action_table_model",
)
class TestSelectFMEA:
    """Class for testing do_select() and do_select_all() methods."""

    def on_succeed_on_select_all(self, tree):
        """Listen for succeed_retrieve messages."""
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(TEST_IDS["mode"]).data["fmeca"], RAMSTKModeRecord
        )
        assert isinstance(
            tree.get_node(TEST_IDS["mechanism"]).data["fmeca"], RAMSTKMechanismRecord
        )
        assert isinstance(
            tree.get_node(TEST_IDS["cause"]).data["fmeca"], RAMSTKCauseRecord
        )
        assert isinstance(
            tree.get_node(TEST_IDS["control"]).data["fmeca"], RAMSTKControlRecord
        )
        assert isinstance(
            tree.get_node(TEST_IDS["action"]).data["fmeca"], RAMSTKActionRecord
        )
        print("\033[36m\n\tsucceed_retrieve_fmeca topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        test_view_model,
        test_mode_table_model,
        test_mechanism_table_model,
        test_cause_table_model,
        test_control_table_model,
        test_action_table_model,
    ):
        """Should return tree of modes, mechanisms, causess, controls, actions."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmeca")

        test_mode_table_model.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_mechanism_table_model.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_cause_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_control_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_action_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mode"]).data["fmeca"],
            RAMSTKModeRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mechanism"]).data["fmeca"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["cause"]).data["fmeca"],
            RAMSTKCauseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["control"]).data["fmeca"],
            RAMSTKControlRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["action"]).data["fmeca"],
            RAMSTKActionRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmeca")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self,
        test_view_model,
        test_mode_table_model,
        test_mechanism_table_model,
        test_cause_table_model,
        test_control_table_model,
        test_action_table_model,
    ):
        """Should clear existing nodes from the records tree and then re-populate."""
        test_mode_table_model.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_mechanism_table_model.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_cause_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            }
        )
        test_control_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_action_table_model.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mode"]).data["fmeca"],
            RAMSTKModeRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mechanism"]).data["fmeca"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["cause"]).data["fmeca"],
            RAMSTKCauseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["control"]).data["fmeca"],
            RAMSTKControlRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["action"]).data["fmeca"],
            RAMSTKActionRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmeca")

        test_view_model.on_select_all()

        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mode"]).data["fmeca"],
            RAMSTKModeRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["mechanism"]).data["fmeca"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["cause"]).data["fmeca"],
            RAMSTKCauseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["control"]).data["fmeca"],
            RAMSTKControlRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node(TEST_IDS["action"]).data["fmeca"],
            RAMSTKActionRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_fmeca")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self,
        test_view_model,
        test_mode_table_model,
        test_mechanism_table_model,
        test_cause_table_model,
        test_control_table_model,
        test_action_table_model,
    ):
        """Should return an empty records tree if the base tree is empty."""
        test_view_model._dic_trees["mode"] = Tree()

        assert test_view_model.on_select_all() is None
        assert test_view_model.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mode_table_model",
    "test_mechanism_table_model",
    "test_cause_table_model",
    "test_control_table_model",
    "test_action_table_model",
)
class TestInsertFMEA:
    """Class for testing the FMEA do_insert() method."""

    def on_succeed_insert_mode(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("7")
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on mode insert.")

    def on_succeed_insert_mechanism(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("6.5")
        print(
            "\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on mechanism insert."
        )

    def on_succeed_insert_cause(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.5")
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on cause insert.")

    def on_succeed_insert_control(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.3.5c")
        print(
            "\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on control insert."
        )

    def on_succeed_insert_action(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("6.3.3.5a")
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on action insert.")

    @pytest.mark.integration
    def test_do_insert_mode(self, test_view_model):
        """Should add a new mode record to the records tree."""
        assert not test_view_model.tree.contains("7")

        pub.subscribe(self.on_succeed_insert_mode, "succeed_retrieve_fmea")

        pub.sendMessage(
            "request_insert_mode",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
            },
        )

        assert test_view_model.tree.contains("7")

        pub.unsubscribe(self.on_succeed_insert_mode, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_mechanism(self, test_view_model):
        """Should add a new mechanism record to the records tree."""
        assert not test_view_model.tree.contains("6.5")

        pub.subscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_fmea")

        pub.sendMessage(
            "request_insert_mechanism",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
            },
        )

        assert test_view_model.tree.contains("6.5")

        pub.unsubscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_cause(self, test_view_model):
        """Should add a new cause record to the records tree."""
        assert not test_view_model.tree.contains("6.3.5")

        pub.subscribe(self.on_succeed_insert_cause, "succeed_retrieve_fmea")

        pub.sendMessage(
            "request_insert_cause",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
                "description": "Test Failure Cause #1 for Mechanism ID 3",
            },
        )

        assert test_view_model.tree.contains("6.3.5")

        pub.unsubscribe(self.on_succeed_insert_cause, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_control(self, test_view_model):
        """Should add a new control record to the records tree."""
        assert not test_view_model.tree.contains("6.3.3.5c")

        pub.subscribe(self.on_succeed_insert_control, "succeed_retrieve_fmea")

        pub.sendMessage(
            "request_insert_control",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
                "control_id": 3,
            },
        )

        assert test_view_model.tree.contains("6.3.3.5c")

        pub.unsubscribe(self.on_succeed_insert_control, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_insert_action(self, test_view_model):
        """Should add a new action record to the records tree."""
        assert not test_view_model.tree.contains("6.3.3.5a")

        pub.subscribe(self.on_succeed_insert_action, "succeed_retrieve_fmea")

        pub.sendMessage(
            "request_insert_action",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
                "action_id": 1,
            },
        )

        assert test_view_model.tree.contains("6.3.3.5a")

        pub.unsubscribe(self.on_succeed_insert_action, "succeed_retrieve_fmea")


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mode_table_model",
    "test_mechanism_table_model",
    "test_cause_table_model",
    "test_control_table_model",
    "test_action_table_model",
)
class TestDeleteFMEA:
    """Class for testing the FMEA do_delete() method."""

    def on_succeed_delete_action(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains(TEST_IDS["action"])
        assert tree.contains(TEST_IDS["control"])
        assert tree.contains(TEST_IDS["cause"])
        assert tree.contains(TEST_IDS["mechanism"])
        assert tree.contains(TEST_IDS["mode"])
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on action delete.")

    def on_succeed_delete_control(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.contains(TEST_IDS["mode"])
        assert tree.contains(TEST_IDS["mechanism"])
        assert tree.contains(TEST_IDS["cause"])
        assert not tree.contains("6.3.3.4c")
        assert tree.contains("6.3.3.4a")
        print(
            "\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on control delete."
        )

    def on_succeed_delete_cause(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.contains(TEST_IDS["mode"])
        assert tree.contains(TEST_IDS["mechanism"])
        assert not tree.contains(TEST_IDS["cause"])
        assert not tree.contains("6.3.3.4c")
        assert not tree.contains("6.3.3.4a")
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on cause delete.")

    def on_succeed_delete_mechanism(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.contains(TEST_IDS["mode"])
        assert not tree.contains(TEST_IDS["mechanism"])
        print(
            "\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on mechanism delete."
        )

    def on_succeed_delete_mode(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("4")
        assert tree.contains("5")
        assert not tree.contains(TEST_IDS["mode"])
        print("\033[36m\n\tsucceed_retrieve_fmea topic was broadcast on mode delete.")

    @pytest.mark.integration
    def test_do_delete_action(self, test_view_model):
        """Should remove the deleted action record from the records tree."""
        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert test_view_model.tree.contains(TEST_IDS["cause"])
        assert test_view_model.tree.contains(TEST_IDS["control"])
        assert test_view_model.tree.contains(TEST_IDS["action"])

        pub.subscribe(self.on_succeed_delete_action, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_action", node_id=3)

        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert test_view_model.tree.contains(TEST_IDS["cause"])
        assert test_view_model.tree.contains(TEST_IDS["control"])
        assert not test_view_model.tree.contains(TEST_IDS["action"])
        assert test_view_model.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_action, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_control(self, test_view_model):
        """Should remove the deleted control record from the records tree."""
        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert test_view_model.tree.contains(TEST_IDS["cause"])
        assert test_view_model.tree.contains("6.3.3.4c")
        assert test_view_model.tree.contains("6.3.3.4a")

        pub.subscribe(self.on_succeed_delete_control, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_control", node_id=4)

        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert test_view_model.tree.contains(TEST_IDS["cause"])
        assert not test_view_model.tree.contains("6.3.3.4c")
        assert test_view_model.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_control, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_cause(self, test_view_model):
        """Should remove the deleted cause record from the records tree."""
        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert test_view_model.tree.contains(TEST_IDS["cause"])
        assert not test_view_model.tree.contains("6.3.3.4c")
        assert test_view_model.tree.contains("6.3.3.4a")

        pub.subscribe(self.on_succeed_delete_cause, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_cause", node_id=3)

        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])
        assert not test_view_model.tree.contains(TEST_IDS["cause"])
        assert not test_view_model.tree.contains("6.3.3.4c")
        assert not test_view_model.tree.contains("6.3.3.4a")

        pub.unsubscribe(self.on_succeed_delete_cause, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_mechanism(self, test_view_model):
        """Should remove the deleted mechanism record from the records tree."""
        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert test_view_model.tree.contains(TEST_IDS["mechanism"])

        pub.subscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_mechanism", node_id=3)

        assert test_view_model.tree.contains(TEST_IDS["mode"])
        assert not test_view_model.tree.contains(TEST_IDS["mechanism"])

        pub.unsubscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_fmea")

    @pytest.mark.integration
    def test_do_delete_mode(self, test_view_model):
        """Should remove the deleted mode record from the records tree."""
        assert test_view_model.tree.contains(TEST_IDS["mode"])

        pub.subscribe(self.on_succeed_delete_mode, "succeed_retrieve_fmea")

        pub.sendMessage("request_delete_mode", node_id=6)

        assert not test_view_model.tree.contains(TEST_IDS["mode"])

        pub.unsubscribe(self.on_succeed_delete_mode, "succeed_retrieve_fmea")
