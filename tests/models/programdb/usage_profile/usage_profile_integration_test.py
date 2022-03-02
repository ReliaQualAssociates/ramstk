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
from ramstk.models.dbtables import (
    RAMSTKEnvironmentTable,
    RAMSTKMissionPhaseTable,
    RAMSTKMissionTable,
)
from ramstk.models.dbviews import RAMSTKUsageProfileView


@pytest.fixture(scope="class")
def test_mission(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_phase(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionPhaseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut.do_insert, "request_insert_mission_phase")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_environment(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKEnvironmentTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_viewmodel():
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKUsageProfileView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission_phase")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_environments")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_missions")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_mission_phases")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_viewmodel", "test_mission", "test_phase", "test_environment"
)
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_on_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("1").data["usage_profile"], RAMSTKMissionRecord)
        assert isinstance(
            tree.get_node("1.1").data["usage_profile"], RAMSTKMissionPhaseRecord
        )
        assert isinstance(
            tree.get_node("1.1.1").data["usage_profile"], RAMSTKEnvironmentRecord
        )
        print("\033[36m\nsucceed_retrieve_usage_profile topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should return records tree with missions, mission phases, environments."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_viewmodel.tree.get_node("1").data["usage_profile"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("2").data["usage_profile"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_viewmodel.tree.get_node("2.2").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("2.2.2").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("3").data["usage_profile"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_viewmodel.tree.get_node("3.3").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("3.3.3").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

    @pytest.mark.integration
    def test_on_select_all_tree_loaded(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should clear existing nodes from the records tree and then re-populate."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_viewmodel.tree.get_node("1").data["usage_profile"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

        test_viewmodel.on_select_all()

        assert isinstance(
            test_viewmodel.tree.get_node("1").data["usage_profile"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1").data["usage_profile"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node("1.1.1").data["usage_profile"],
            RAMSTKEnvironmentRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_usage_profile")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should return an empty records tree if the base tree is empty."""
        test_viewmodel._dic_trees["mission"] = Tree()

        assert test_viewmodel.on_select_all() is None
        assert test_viewmodel.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_viewmodel", "test_mission", "test_phase", "test_environment"
)
class TestInsertMethods:
    """Class for testing the on_insert() method."""

    def on_succeed_insert_mission(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("4")
        print("\033[36m\nsucceed_insert_mission topic was broadcast on mission insert.")

    def on_succeed_insert_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("1.4")
        print(
            "\033[36m\nsucceed_insert_mission_phase topic was broadcast on mission "
            "phase insert."
        )

    def on_succeed_insert_environment(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("1.1.4")
        print(
            "\033[36m\nsucceed_insert_environment topic was broadcast on "
            "environment insert."
        )

    @pytest.mark.integration
    def test_do_insert_mission(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should add a new mission record to the records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 1})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert not test_viewmodel.tree.contains("4")

        pub.subscribe(self.on_succeed_insert_mission, "succeed_retrieve_usage_profile")

        pub.sendMessage(
            "request_insert_mission",
            attributes={
                "revision_id": 1,
                "mission_id": 1,
                "parent_id": 1,
                "record_id": 1,
            },
        )

        pub.unsubscribe(
            self.on_succeed_insert_mission, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_mission_phase(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should add a new mission phase record to the records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 1})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert not test_viewmodel.tree.contains("1.4")

        pub.subscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage(
            "request_insert_mission_phase",
            attributes={
                "revision_id": 1,
                "mission_id": 1,
                "mission_phase_id": 1,
                "parent_id": 1,
                "record_id": 1,
            },
        )

        assert test_viewmodel.tree.contains("1.4")

        pub.unsubscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_environment(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should add a new environment record to the records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 1})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_id": 1, "mission_phase_id": 1}
        )

        assert not test_viewmodel.tree.contains("1.1.4")

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
                "parent_id": 1,
                "record_id": 1,
                "name": "Condition Name",
            },
        )

        assert test_viewmodel.tree.contains("1.1.4")

        pub.unsubscribe(
            self.on_succeed_insert_environment, "succeed_retrieve_usage_profile"
        )


@pytest.mark.usefixtures(
    "test_viewmodel", "test_mission", "test_phase", "test_environment"
)
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete_mission(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("1.1.1")
        assert not tree.contains("1.1")
        assert not tree.contains("1")
        print(
            "\033[36m\nsucceed_retrieve_usage_profile topic was broadcast on mission "
            "delete."
        )

    def on_succeed_delete_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("2.2.2")
        assert not tree.contains("2.2")
        assert tree.contains("2")
        print(
            "\033[36m\nsucceed_retrieve_usage_profile topic was broadcast on mission "
            "phase delete."
        )

    def on_succeed_delete_environment(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains("3.3.3")
        assert tree.contains("3.3")
        assert tree.contains("3")
        print(
            "\033[36m\nsucceed_retrieve_usage_profile topic was broadcast on "
            "environment delete."
        )

    @pytest.mark.integration
    def test_do_delete_environment(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should remove deleted environment record from the records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 3})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 3}
        )

        assert test_viewmodel.tree.contains("3.3.3")
        assert test_viewmodel.tree.contains("3.3")
        assert test_viewmodel.tree.contains("3")

        pub.subscribe(
            self.on_succeed_delete_environment, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage("request_delete_environment", node_id=3)

        pub.unsubscribe(
            self.on_succeed_delete_environment, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_delete_mission_phase(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should remove deleted phase and environment records from records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 2})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 2}
        )

        assert test_viewmodel.tree.contains("2.2.2")
        assert test_viewmodel.tree.contains("2.2")
        assert test_viewmodel.tree.contains("2")

        pub.subscribe(
            self.on_succeed_delete_mission_phase, "succeed_retrieve_usage_profile"
        )

        pub.sendMessage("request_delete_mission_phase", node_id=2)

        pub.unsubscribe(
            self.on_succeed_delete_mission_phase, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_delete_mission(
        self, test_viewmodel, test_mission, test_phase, test_environment
    ):
        """should remove deleted mission, phase, and environment from records tree."""
        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1, "mission_id": 1})
        test_environment.do_select_all(
            attributes={"revision_id": 1, "mission_phase_id": 1}
        )

        assert test_viewmodel.tree.contains("1.1.1")
        assert test_viewmodel.tree.contains("1.1")
        assert test_viewmodel.tree.contains("1")

        pub.subscribe(self.on_succeed_delete_mission, "succeed_retrieve_usage_profile")

        pub.sendMessage("request_delete_mission", node_id=1)

        pub.unsubscribe(
            self.on_succeed_delete_mission, "succeed_retrieve_usage_profile"
        )
