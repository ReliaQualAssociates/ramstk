# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.validation.validation_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module integrations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKValidationRecord
from ramstk.models.dbtables import RAMSTKValidationTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectValidation(SystemTestSelectMethods):
    """Class for testing Validation table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKValidationRecord
    _select_id = 1
    _tag = "validation"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertValidation(SystemTestInsertMethods):
    """Class for testing Validation table do_insert() method."""

    __test__ = True

    _insert_id = 4
    _record = RAMSTKValidationRecord
    _tag = "validation"

    @pytest.mark.skip(reason="Validation records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Validations are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Validation records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Validations are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteValidation(SystemTestDeleteMethods):
    """Class for testing Validation table do_delete() method."""

    __test__ = True

    _delete_id = 2
    _record = RAMSTKValidationRecord
    _tag = "validation"

    @pytest.mark.skip(reason="Validation records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Validations are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateValidation:
    """Class for testing Validation table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKValidationRecord
    _tag = "validation"
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
            f"The value for one or more attributes for {self._tag} ID "
            f"{self._update_id} was the wrong type."
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

        _validation = integration_test_table_model.do_select(self._update_id)
        _validation.name = "Test Validation"
        _validation.time_maximum = 10.5
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

        _validation = integration_test_table_model.do_select(self._update_id)
        _validation.description = "Big test validation #1"
        _validation = integration_test_table_model.do_select(self._update_id + 1)
        _validation.description = "Big test validation #2"

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.do_select(self._update_id).description
            == "Big test validation #1"
        )
        assert (
            integration_test_table_model.do_select(self._update_id + 1).description
            == "Big test validation #2"
        )

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

        _validation = integration_test_table_model.do_select(self._update_id)
        _validation.time_mean = {1: 2}
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
    def test_do_update_non_existent_id(self):
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
class TestGetterSetterValidation(SystemTestGetterSetterMethods):
    """Class for testing Validation table getter and setter methods."""

    __test__ = True

    _package = {"task_specification": "MIL-HDBK-217F"}
    _record = RAMSTKValidationRecord
    _tag = "validation"
    _test_id = 1


@pytest.mark.usefixtures("integration_test_table_model")
class TestAnalysisValidation:
    """Class for testing Validation analytical methods."""

    def on_succeed_calculate_all_tasks(self, tree):
        """Listen for succeed_calculate messages."""
        assert isinstance(tree, Tree)
        print("\033[36m\n\tsucceed_calculate_all_tasks topic was broadcast.")

    def on_succeed_calculate_plan(self, attributes):
        """Listen for succeed_calculate messages."""
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() - timedelta(days=10)), "lower"
        ] == pytest.approx(31.0004501932)
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() + timedelta(days=20)), "mean"
        ] == pytest.approx(21.6666667)
        assert (
            attributes["plan"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "upper"
            ]
            == 0.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "lower"
            ]
            == 55.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "mean"
            ]
            == 70.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "upper"
            ]
            == 100.0
        )
        print("\033[36m\n\tsucceed_calculate_verification_plan topic was broadcast")

    @pytest.mark.integration
    def test_do_calculate_all_tasks(self, integration_test_table_model):
        """Should calculate all the validation tasks time and cost."""
        pub.subscribe(
            self.on_succeed_calculate_all_tasks,
            "succeed_calculate_all_validation_tasks",
        )

        _validation = integration_test_table_model.do_select(1)
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation = integration_test_table_model.do_select(2)
        _validation.time_minimum = 30.0
        _validation.time_average = 60.0
        _validation.time_maximum = 80.0
        _validation.cost_minimum = 850.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 3500.0
        _validation.confidence = 95.0

        pub.sendMessage("request_calculate_all_validation_tasks")

        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_ll == pytest.approx(11.86684674)
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_mean == pytest.approx(21.66666667)
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_ul == pytest.approx(31.46648659)
        assert (
            integration_test_table_model.tree.get_node(1)
            .data["validation"]
            .time_variance
            == 25.0
        )
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_ll == pytest.approx(1659.34924016)
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_mean == pytest.approx(2525.0)
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_ul == pytest.approx(3390.65075984)
        assert integration_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].time_ll == pytest.approx(42.00030013)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].time_mean == pytest.approx(58.33333333)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].time_ul == pytest.approx(74.66636654)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].time_variance == pytest.approx(69.44444444)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].cost_ll == pytest.approx(659.34924016)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].cost_mean == pytest.approx(1525.0)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].cost_ul == pytest.approx(2390.65075984)
        assert integration_test_table_model.tree.get_node(2).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)

        pub.unsubscribe(
            self.on_succeed_calculate_all_tasks,
            "succeed_calculate_all_validation_tasks",
        )

    @pytest.mark.integration
    def test_do_calculate_verification_plan(self, integration_test_table_model):
        """Should calculate the planned validation effort time and cost."""
        pub.subscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )

        _validation = integration_test_table_model.do_select(1)
        _validation.acceptable_minimum = 55.0
        _validation.acceptable_mean = 70.0
        _validation.acceptable_maximum = 100.0
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation.status = 0.5
        _validation.task_type = 5
        _validation = integration_test_table_model.do_select(2)
        _validation.acceptable_minimum = 125.0
        _validation.acceptable_mean = 160.0
        _validation.acceptable_maximum = 190.0
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        _validation.status = 0.2

        pub.sendMessage("request_calculate_plan")

        pub.unsubscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )

    @pytest.mark.integration
    def test_do_calculate_verification_plan_with_mean_time(
        self, integration_test_table_model
    ):
        """Should calculate the planned validation effort time and cost."""
        _validation = integration_test_table_model.do_select(1)
        _validation.acceptable_minimum = 55.0
        _validation.acceptable_mean = 70.0
        _validation.acceptable_maximum = 100.0
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 10.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation.status = 0.5
        _validation.task_type = 5
        _validation = integration_test_table_model.do_select(2)
        _validation.acceptable_minimum = 125.0
        _validation.acceptable_mean = 160.0
        _validation.acceptable_maximum = 190.0
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        _validation.status = 0.2

        pub.sendMessage("request_calculate_plan")
