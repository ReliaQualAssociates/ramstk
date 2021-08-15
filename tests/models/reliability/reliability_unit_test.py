# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.reliability.reliability_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Reliability module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKReliabilityTable
from ramstk.models.programdb import RAMSTKReliability


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKReliabilityTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_reliability_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_reliability_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_reliability")
    pub.unsubscribe(dut.do_update, "request_update_reliability")
    pub.unsubscribe(dut.do_get_tree, "request_get_reliability_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_reliability")
    pub.unsubscribe(dut.do_insert, "request_insert_reliability")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKReliabilityTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_reliability"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "reliability"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKReliability
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_reliability_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_reliability_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_reliability"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_reliability"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_reliability_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_reliability")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_reliability")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_reliability")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["reliability"],
            RAMSTKReliability,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["reliability"],
            RAMSTKReliability,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["reliability"],
            RAMSTKReliability,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)

        assert isinstance(_reliability, RAMSTKReliability)
        assert _reliability.revision_id == 1
        assert _reliability.hardware_id == 1
        assert _reliability.hazard_rate_active == 0.0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKReliability)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["reliability"],
            RAMSTKReliability,
        )
        assert test_tablemodel.tree.get_node(4).data["reliability"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["reliability"].hardware_id == 4


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(node_id=_last_id)

        assert test_tablemodel.last_id == 2
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_specified_ht(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_specified = 0.0032
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0)

        assert _reliability.hazard_rate_active == pytest.approx(0.0032)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_specified_mtbf(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate when MTBF is specified."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 3
        _reliability.mtbf_specified = 12632.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0)

        assert _reliability.hazard_rate_active == pytest.approx(7.9164028e-05)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_exponential(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate for the EXP."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 1
        _reliability.scale_parameter = 10000.0
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        # One-parameter EXP.
        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0)
        assert _reliability.hazard_rate_active == 0.0001

        # Two-parameter EXP.
        _reliability.failure_distribution_id = 2
        _reliability.scale_parameter = 1000.0
        _reliability.location_parameter = 56.0

        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.0009469697)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_lognormal(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate for the LOGN at time."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 3
        _reliability.scale_parameter = 33.65
        _reliability.shape_parameter = 0.9663
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        # Two-parameter LOGN.
        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0, time=4.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.6610467)

        # Three-parameter LOGN.
        _reliability.failure_distribution_id = 4
        _reliability.location_parameter = 1.85

        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0, time=4.0)
        assert _reliability.hazard_rate_active == pytest.approx(1.5117773)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_normal(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate for the NORM at time."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 5
        _reliability.scale_parameter = 10.0
        _reliability.shape_parameter = 0.0
        _reliability.location_parameter = 100.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        # Two-parameter NORM.
        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0, time=85.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.01387898)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_weibull(
        self, test_attributes, test_tablemodel
    ):
        """should calculate the active hazard rate for the WEI at time."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 6
        _reliability.scale_parameter = 525.0
        _reliability.shape_parameter = 2.5
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        # Two-parameter WEI.
        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0, time=105.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.0235972)

        # Three-parameter WEI.
        _reliability.failure_distribution_id = 7
        _reliability.location_parameter = 18.5
        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0, time=105.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.02874279)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_logistics(self, test_attributes, test_tablemodel):
        """should calculate the logistics hazard rate."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_active = 0.0032
        _reliability.hazard_rate_dormant = 0.000128
        _reliability.hazard_rate_software = 0.00005

        test_tablemodel.do_calculate_hazard_rate_logistics(1)

        assert _reliability.hazard_rate_logistics == pytest.approx(0.003378)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_no_type(self, test_attributes, test_tablemodel):
        """should return zero for the active hazard rate when unknown type ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 5
        _reliability.hazard_rate_specified = 0.0032
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0

        test_tablemodel.do_calculate_hazard_rate_active(1, 100.0, 1, 1.0)

        assert _reliability.hazard_rate_active == 0.0

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_logistics(self, test_attributes, test_tablemodel):
        """should calculate the logistics hazard rate."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_active = 0.0032
        _reliability.hazard_rate_dormant = 0.000128
        _reliability.hazard_rate_software = 0.00005

        test_tablemodel.do_calculate_hazard_rate_logistics(1)

        assert _reliability.hazard_rate_logistics == pytest.approx(0.003378)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_mission(self, test_attributes, test_tablemodel):
        """should calculate the mission hazard rate."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_active = 0.0032
        _reliability.hazard_rate_dormant = 0.000128
        _reliability.hazard_rate_software = 0.00005

        test_tablemodel.do_calculate_hazard_rate_mission(1, 0.55)

        assert _reliability.hazard_rate_mission == pytest.approx(0.0018676)

    @pytest.mark.unit
    def test_do_calculate_mtbf(self, test_attributes, test_tablemodel):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 0.003378
        _reliability.hazard_rate_mission = 0.0018676

        test_tablemodel.do_calculate_mtbf(1, 1.0)

        assert _reliability.mtbf_logistics == pytest.approx(296.03315571)
        assert _reliability.mtbf_mission == pytest.approx(535.4465624)

    @pytest.mark.unit
    def test_do_calculate_mtbf_zero_logistics(self, test_attributes, test_tablemodel):
        """should return 0.0 when the logistics hazard rate = 0.0."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 0.0
        _reliability.hazard_rate_mission = 0.0018676

        test_tablemodel.do_calculate_mtbf(1, 1.0)

        assert _reliability.mtbf_logistics == 0.0
        assert _reliability.mtbf_mission == pytest.approx(535.4465624)

    @pytest.mark.unit
    def test_do_calculate_mtbf_zero_mission(self, test_attributes, test_tablemodel):
        """should return 0.0 when the logistics hazard rate = 0.0."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 0.003378
        _reliability.hazard_rate_mission = 0.0

        test_tablemodel.do_calculate_mtbf(1, 1.0)

        assert _reliability.mtbf_logistics == pytest.approx(296.03315571)
        assert _reliability.mtbf_mission == 0.0

    @pytest.mark.unit
    def test_do_calculate_reliability(self, test_attributes, test_tablemodel):
        """should calculate the active hazard rate for the EXP."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_logistics = 0.003378
        _reliability.hazard_rate_mission = 0.0018676

        test_tablemodel.do_calculate_reliability(1, 1.0)
        assert _reliability.reliability_logistics == pytest.approx(0.9966277)
        assert _reliability.reliability_mission == pytest.approx(0.9981341)
