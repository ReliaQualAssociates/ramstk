# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.usage_profile.usage_profile_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Usage Profile integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKEnvironmentRecord,
    RAMSTKMissionPhaseRecord,
    RAMSTKMissionRecord,
)


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mission_table_model",
    "test_mission_phase_table_model",
    "test_environment_table_model",
    "test_suite_logger",
)
class TestSelectUsageProfile:
    """Class for testing Usage Profile do_select() and do_select_all() methods."""

    def on_succeed_on_select_all(self, tree):
        """Listen for succeed_retrieve messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("1").data["usage_profile"], RAMSTKMissionRecord)
        assert isinstance(
            tree.get_node("1.1").data["usage_profile"], RAMSTKMissionPhaseRecord
        )
        assert isinstance(
            tree.get_node("1.1.1").data["usage_profile"], RAMSTKEnvironmentRecord
        )
        print("\033[36m\n\tsucceed_retrieve_usage_profile topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should return records tree with missions, mission phases, environments."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(attributes={"revision_id": 1})
        test_environment_table_model.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_view_model.tree.get_node("1").data["usage_profile"],
            RAMSTKMissionRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("2").data["usage_profile"],
            RAMSTKMissionRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("2.2").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("2.2.2").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("3").data["usage_profile"],
            RAMSTKMissionRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("3.3").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("3.3.3").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should clear existing nodes from the records tree and then re-populate."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(attributes={"revision_id": 1})
        test_environment_table_model.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_view_model.tree.get_node("1").data["usage_profile"],
            RAMSTKMissionRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

        test_view_model.on_select_all()

        assert isinstance(
            test_view_model.tree.get_node("1").data["usage_profile"],
            RAMSTKMissionRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_view_model.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should return an empty records tree if the base tree is empty."""
        test_view_model._dic_trees["mission"] = Tree()

        assert test_view_model.on_select_all() is None
        assert test_view_model.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mission_table_model",
    "test_mission_phase_table_model",
    "test_environment_table_model",
    "test_suite_logger",
)
class TestInsertUsageProfile:
    """Class for testing the Usage Profile on_insert() method."""

    def on_succeed_insert_mission(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("4")
        print(
            "\033[36m\n\tsucceed_insert_mission topic was broadcast on mission insert."
        )

    def on_succeed_insert_mission_phase(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("1.4")
        print(
            "\033[36m\n\tsucceed_insert_mission_phase topic was broadcast on mission "
            "phase insert."
        )

    def on_succeed_insert_environment(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains("1.1.4")
        print(
            "\033[36m\n\tsucceed_insert_environment topic was broadcast on "
            "environment insert."
        )

    @pytest.mark.integration
    def test_do_insert_mission(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should add a new mission record to the records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert not test_view_model.tree.contains("4")

        pub.subscribe(self.on_succeed_insert_mission, "succeed_retrieve_usage_profile")

        pub.sendMessage(
            "request_insert_mission",
            attributes={
                "revision_id": 1,
                "mission_id": 1,
            },
        )

        pub.unsubscribe(
            self.on_succeed_insert_mission, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_mission_phase(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should add a new mission phase record to the records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert not test_view_model.tree.contains("1.4")

        pub.subscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage(
            "request_insert_mission_phase",
            attributes={
                "revision_id": 1,
                "mission_id": 1,
                "mission_phase_id": 1,
            },
        )

        assert test_view_model.tree.contains("1.4")

        pub.unsubscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_environment(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should add a new environment record to the records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1, "mission_phase_id": 1}
        )

        assert not test_view_model.tree.contains("1.1.4")

        pub.subscribe(
            self.on_succeed_insert_environment, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage(
            "request_insert_environment",
            attributes={
                "revision_id": 1,
                "mission_id": 1,
                "mission_phase_id": 1,
                "environment_id": 1,
                "name": "Condition Name",
            },
        )

        assert test_view_model.tree.contains("1.1.4")

        pub.unsubscribe(
            self.on_succeed_insert_environment, "succeed_retrieve_usage_profile"
        )


@pytest.mark.usefixtures(
    "test_view_model",
    "test_mission_table_model",
    "test_mission_phase_table_model",
    "test_environment_table_model",
    "test_suite_logger",
)
class TestDeleteUsageProfile:
    """Class for testing the Usage Profile do_delete() method."""

    def on_succeed_delete_mission(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("1.1.1")
        assert not tree.contains("1.1")
        assert not tree.contains("1")
        print(
            "\033[36m\n\tsucceed_retrieve_usage_profile topic was broadcast on mission "
            "delete."
        )

    def on_succeed_delete_mission_phase(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("2.2.2")
        assert not tree.contains("2.2")
        assert tree.contains("2")
        print(
            "\033[36m\n\tsucceed_retrieve_usage_profile topic was broadcast on mission "
            "phase delete."
        )

    def on_succeed_delete_environment(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\n\tsucceed_retrieve_usage_profile topic was broadcast on "
            "environment delete."
        )

    @pytest.mark.integration
    def test_do_delete_environment(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should remove deleted environment record from the records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 3}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 3}
        )

        assert test_view_model.tree.contains("3.3.3")
        assert test_view_model.tree.contains("3.3")
        assert test_view_model.tree.contains("3")

        pub.subscribe(
            self.on_succeed_delete_environment, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage("request_delete_environment", node_id=3)

        pub.unsubscribe(
            self.on_succeed_delete_environment, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_delete_mission_phase(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should remove deleted phase and environment records from records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 2}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 2}
        )

        assert test_view_model.tree.contains("2.2.2")
        assert test_view_model.tree.contains("2.2")
        assert test_view_model.tree.contains("2")

        pub.subscribe(
            self.on_succeed_delete_mission_phase, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage("request_delete_mission_phase", node_id=2)

        pub.unsubscribe(
            self.on_succeed_delete_mission_phase, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_delete_mission(
        self,
        test_view_model,
        test_mission_table_model,
        test_mission_phase_table_model,
        test_environment_table_model,
    ):
        """Should remove deleted mission, phase, and environment from records tree."""
        test_mission_table_model.do_select_all(attributes={"revision_id": 1})
        test_mission_phase_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1}
        )
        test_environment_table_model.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert test_view_model.tree.contains("1.1.1")
        assert test_view_model.tree.contains("1.1")
        assert test_view_model.tree.contains("1")

        pub.subscribe(self.on_succeed_delete_mission, "succeed_retrieve_usage_profile")

        pub.sendMessage("request_delete_mission", node_id=1)

        pub.unsubscribe(
            self.on_succeed_delete_mission, "succeed_retrieve_usage_profile"
        )
