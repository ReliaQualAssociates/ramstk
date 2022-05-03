# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_status.program_status_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module integrations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramStatusRecord
from ramstk.models.dbtables import RAMSTKProgramStatusTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectProgramStatus(SystemTestSelectMethods):
    """Class for testing Prog Status table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKProgramStatusRecord
    _select_id = 1
    _tag = "program_status"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertProgramStatus(SystemTestInsertMethods):
    """Class for testing Program Status table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"

    def on_fail_insert_duplicate_date(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            f"do_insert: Database error when attempting to add a "
            f"record.  Database returned:\n\tKey (fld_date_status)=({date.today()}) "
            f"already exists."
        )

        print(
            f"\033[35m\n\tfail_insert_{self._tag} topic was broadcast on duplicate "
            f"date."
        )

    @pytest.mark.skip(reason="Program Status records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Program Statuses are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Program Status records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Program Statuses are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Program Status records are non-hierarchical.")
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should not run because Program Statuses are not hierarchical."""
        pass

    @pytest.mark.integration
    def test_do_insert_duplicate_date(
        self, test_attributes, integration_test_table_model
    ):
        """Should not add a record if date is being duplicated."""
        pub.subscribe(
            self.on_fail_insert_duplicate_date,
            "do_log_debug_msg",
        )

        test_attributes["date_status"] = date.today()
        pub.sendMessage(
            "request_insert_program_status",
            attributes=test_attributes,
        )

        pub.unsubscribe(
            self.on_fail_insert_duplicate_date,
            "do_log_debug_msg",
        )


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteProgramStatus(SystemTestDeleteMethods):
    """Class for testing Program Status table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"

    @pytest.mark.skip(reason="Program Status records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Program Statuses are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateProgramStatus:
    """Class for testing Prog Status table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_update_{self._tag} topic was broadcast.")

    def on_succeed_update_all(self):
        """Listen for succeed_update messages."""
        print(
            f"\033[36m\n\tsucceed_update_all topic was broadcast on update all "
            f"{self._tag}s"
        )

    def on_fail_update_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            f"The value for one or more attributes for {self._tag.replace('_', ' ')} "
            f"ID {self._update_id} was the wrong type."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on wrong data "
            f"type."
        )

    def on_fail_update_root_node(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent "
            f"{self._tag.replace('_', ' ')} with"
            f" {self._tag.replace('_', ' ')} "
            f"ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"No data package found for {self._tag.replace('_', ' ')} ID "
            f"{self._update_id}."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update the attribute value for record ID."""
        pub.subscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].cost_remaining = 47832.00
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].time_remaining = 528.3

        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        pub.unsubscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

        pub.sendMessage(f"request_update_all_{self._tag}")

        pub.unsubscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

        _status = integration_test_table_model.do_select(self._update_id)
        _status.time_remaining = {1: 2}
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        pub.unsubscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_root_node(self, integration_test_table_model):
        """Should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node,
            "do_log_debug_msg",
        )

        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=0,
        )

        pub.unsubscribe(
            self.on_fail_update_root_node,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, integration_test_table_model):
        """Should send the fail message when updating a non-existent record ID."""
        pub.subscribe(
            self.on_fail_update_non_existent_id,
            "do_log_debug_msg",
        )

        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=100,
        )

        pub.unsubscribe(
            self.on_fail_update_non_existent_id,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the fail message when the record ID has no data package."""
        pub.subscribe(
            self.on_fail_update_no_data_package,
            "do_log_debug_msg",
        )

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        pub.unsubscribe(
            self.on_fail_update_no_data_package,
            "do_log_debug_msg",
        )


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterProgramStatus(SystemTestGetterSetterMethods):
    """Class for testing ProgramS tatus table getter and setter methods."""

    __test__ = True

    _package = {"description": "Big test operating stress."}
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"
    _test_id = 1

    def on_succeed_get_attributes(self, attributes):
        """Listen for succeed_get_program_status_tree messages."""
        assert isinstance(attributes, dict)
        assert attributes["status_id"] == 1
        assert attributes["cost_remaining"] == 0.0
        assert attributes["date_status"] == date.today() - timedelta(days=30)
        assert attributes["time_remaining"] == 0.0
        print("\033[36m\n\tsucceed_get_program_status_attributes topic was broadcast.")

    def on_succeed_get_actual_status(self, status):
        """Listen for succeed_get_actual_status messages."""
        assert isinstance(status, pd.DataFrame)
        assert status.loc[pd.to_datetime(date.today()), "cost"] == 14608.45
        assert status.loc[pd.to_datetime(date.today()), "time"] == 469.0
        print("\033[36m\n\tsucceed_get_actual_status topic was broadcast")

    @pytest.mark.integration
    def test_do_set_attributes(self, integration_test_table_model):
        """Should set the value of the attribute requested."""
        pub.subscribe(
            self.on_succeed_set_attributes,
            "succeed_get_program_status_tree",
        )

        integration_test_table_model._revision_id = 1
        pub.sendMessage(
            "succeed_calculate_program_remaining",
            cost_remaining=3284.68,
            time_remaining=186,
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes,
            "succeed_get_program_status_tree",
        )

    @pytest.mark.integration
    def test_do_get_actual_status(self, test_attributes, integration_test_table_model):
        """Should update and return program status."""
        integration_test_table_model._do_set_attributes(
            cost_remaining=14608.45, time_remaining=469.00
        )

        pub.subscribe(
            self.on_succeed_get_actual_status,
            "succeed_get_actual_status",
        )
        pub.sendMessage("request_get_actual_status")

        _node_id = integration_test_table_model._dic_status[date.today()]

        assert (
            integration_test_table_model.tree.get_node(_node_id)
            .data["program_status"]
            .cost_remaining
            == 14608.45
        )
        assert (
            integration_test_table_model.tree.get_node(_node_id)
            .data["program_status"]
            .time_remaining
            == 469.00
        )

        pub.unsubscribe(
            self.on_succeed_get_actual_status,
            "succeed_get_actual_status",
        )
