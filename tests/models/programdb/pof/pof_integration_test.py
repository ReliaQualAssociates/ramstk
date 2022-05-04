# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.pof.pof_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKMechanismRecord,
    RAMSTKOpLoadRecord,
    RAMSTKOpStressRecord,
    RAMSTKTestMethodRecord,
)
from ramstk.models.dbtables import (
    RAMSTKMechanismTable,
    RAMSTKOpLoadTable,
    RAMSTKOpStressTable,
    RAMSTKTestMethodTable,
)
from ramstk.models.dbviews import RAMSTKPoFView


@pytest.mark.usefixtures(
    "integration_test_view_model",
    "test_mechanism",
    "test_opload",
    "test_opstress",
    "test_method",
)
class TestSelectPoF:
    """Class for testing PoF do_select() and do_select_all() methods."""

    def on_succeed_on_select_all(self, tree):
        """Listen for succeed_retrieve messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("3").data["pof"], RAMSTKMechanismRecord)
        assert isinstance(tree.get_node("3.3").data["pof"], RAMSTKOpLoadRecord)
        assert isinstance(tree.get_node("3.3.3s").data["pof"], RAMSTKOpStressRecord)
        assert isinstance(tree.get_node("3.3.3t").data["pof"], RAMSTKTestMethodRecord)
        print("\033[36m\n\tsucceed_retrieve_pof topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should return tree of mechanisms, oploads, opstress, test methods."""
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
                "opload_id": 3,
            }
        )
        test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "opload_id": 3,
            }
        )

        assert isinstance(
            integration_test_view_model.tree.get_node("3").data["pof"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3").data["pof"],
            RAMSTKOpLoadRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3s").data["pof"],
            RAMSTKOpStressRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3t").data["pof"],
            RAMSTKTestMethodRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should clear existing nodes from the records tree and then re-populate."""
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
                "opload_id": 3,
            }
        )
        test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "opload_id": 3,
            }
        )

        assert isinstance(
            integration_test_view_model.tree.get_node("3").data["pof"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3").data["pof"],
            RAMSTKOpLoadRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3s").data["pof"],
            RAMSTKOpStressRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3t").data["pof"],
            RAMSTKTestMethodRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

        integration_test_view_model.on_select_all()

        assert isinstance(
            integration_test_view_model.tree.get_node("3").data["pof"],
            RAMSTKMechanismRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3").data["pof"],
            RAMSTKOpLoadRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3s").data["pof"],
            RAMSTKOpStressRecord,
        )
        assert isinstance(
            integration_test_view_model.tree.get_node("3.3.3t").data["pof"],
            RAMSTKTestMethodRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should return an empty records tree if the base tree is empty."""
        integration_test_view_model._dic_trees["mechanism"] = Tree()

        assert integration_test_view_model.on_select_all() is None
        assert integration_test_view_model.tree.depth() == 0


@pytest.mark.usefixtures(
    "integration_test_view_model",
    "test_mechanism",
    "test_opload",
    "test_opstress",
    "test_method",
)
class TestInsertPoF:
    """Class for testing the PoF do_insert() method."""

    def on_succeed_insert_mechanism(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("5")
        print(
            "\033[36m\n\tsucceed_insert_mechanism topic was broadcast on mechanism "
            "insert."
        )

    def on_succeed_insert_opload(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("5.5")
        print("\033[36m\n\tsucceed_insert_opload topic was broadcast on opload insert.")

    def on_succeed_insert_opstress(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("3.3.5s")
        print(
            "\033[36m\n\tsucceed_insert_opstress topic was broadcast on opstress "
            "insert."
        )

    def on_succeed_insert_test_method(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("3.3.5t")
        print(
            "\033[36m\n\tsucceed_insert_test_method topic was broadcast on test "
            "method insert."
        )

    @pytest.mark.integration
    def test_do_insert_mechanism(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should add a new mechanism record to the records tree."""
        assert not integration_test_view_model.tree.contains("5")

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

        assert integration_test_view_model.tree.contains("5")

        pub.unsubscribe(self.on_succeed_insert_mechanism, "succeed_retrieve_pof")

    @pytest.mark.skip
    def test_do_insert_opload(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should add a new opload record to the records tree."""
        assert not integration_test_view_model.tree.contains("5.5")

        pub.subscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_opload",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 5,
                "opload_id": 5,
            },
        )

        assert integration_test_view_model.tree.contains("5.5")

        pub.unsubscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_opstress(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should add a new opstress record to the records tree."""
        assert not integration_test_view_model.tree.contains("3.3.5s")

        pub.subscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_opstress",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 3,
                "opload_id": 3,
                "opstress_id": 4,
            },
        )

        assert integration_test_view_model.tree.contains("3.3.5s")

        pub.unsubscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_test_method(
        self,
        integration_test_view_model,
        test_mechanism,
        test_opload,
        test_opstress,
        test_method,
    ):
        """Should add a new test method record to the records tree."""
        assert not integration_test_view_model.tree.contains("3.3.5t")

        pub.subscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")

        pub.sendMessage(
            "request_insert_test_method",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 3,
                "opload_id": 3,
                "test_method_id": 4,
            },
        )

        assert integration_test_view_model.tree.contains("3.3.5t")

        pub.unsubscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")


@pytest.mark.usefixtures(
    "integration_test_view_model",
    "test_mechanism",
    "test_opload",
    "test_opstress",
    "test_method",
)
class TestDeleteMethods:
    """Class for testing the PoF do_delete() method."""

    def on_succeed_delete_test_method(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert tree.contains("3.3.3s")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\n\tsucceed_retrieve_pof topic was broadcast on test method "
            "delete."
        )

    def on_succeed_delete_opstress(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\n\tsucceed_retrieve_pof topic was broadcast on opstress delete."
        )

    def on_succeed_delete_opload(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert not tree.contains("3.3")
        assert tree.contains("3")
        print("\033[36m\n\tsucceed_retrieve_pof topic was broadcast on opload delete.")

    def on_succeed_delete_mechanism(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3t")
        assert not tree.contains("3.3.3s")
        assert not tree.contains("3.3")
        assert not tree.contains("3")
        print(
            "\033[36m\n\tsucceed_retrieve_pof topic was broadcast on mechanism delete."
        )

    @pytest.mark.integration
    def test_do_delete_test_method(self, integration_test_view_model):
        """Should remove the deleted test method record from the records tree."""
        assert integration_test_view_model.tree.contains("3")
        assert integration_test_view_model.tree.contains("3.3")
        assert integration_test_view_model.tree.contains("3.3.3s")
        assert integration_test_view_model.tree.contains("3.3.3t")
        assert integration_test_view_model.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_test_method, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_test_method", node_id=3)

        assert integration_test_view_model.tree.contains("3")
        assert integration_test_view_model.tree.contains("3.3")
        assert integration_test_view_model.tree.contains("3.3.3s")
        assert not integration_test_view_model.tree.contains("3.3.3t")
        assert integration_test_view_model.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_test_method, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_delete_opstress(self, integration_test_view_model):
        """Should remove deleted opstress and test method records from records tree."""
        assert integration_test_view_model.tree.contains("3")
        assert integration_test_view_model.tree.contains("3.3")
        assert integration_test_view_model.tree.contains("3.3.3s")
        assert integration_test_view_model.tree.contains("3.3.4s")
        assert integration_test_view_model.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_opstress, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_opstress", node_id=3)

        assert integration_test_view_model.tree.contains("3")
        assert integration_test_view_model.tree.contains("3.3")
        assert not integration_test_view_model.tree.contains("3.3.3s")
        assert integration_test_view_model.tree.contains("3.3.4s")
        assert integration_test_view_model.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_opstress, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_delete_opload(self, integration_test_view_model):
        """Should remove the deleted opload record from the records tree."""
        assert integration_test_view_model.tree.contains("3")
        assert integration_test_view_model.tree.contains("3.3")
        assert integration_test_view_model.tree.contains("3.3.4s")
        assert integration_test_view_model.tree.contains("3.3.4t")

        pub.subscribe(self.on_succeed_delete_opload, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_opload", node_id=3)

        assert integration_test_view_model.tree.contains("3")
        assert not integration_test_view_model.tree.contains("3.3")
        assert not integration_test_view_model.tree.contains("3.3.4s")
        assert not integration_test_view_model.tree.contains("3.3.4t")

        pub.unsubscribe(self.on_succeed_delete_opload, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_delete_mechanism(self, integration_test_view_model):
        """Should remove the deleted mechanism record from the records tree."""
        assert integration_test_view_model.tree.contains("3")

        pub.subscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_pof")

        pub.sendMessage("request_delete_mechanism", node_id=3)

        assert not integration_test_view_model.tree.contains("3")

        pub.unsubscribe(self.on_succeed_delete_mechanism, "succeed_retrieve_pof")
