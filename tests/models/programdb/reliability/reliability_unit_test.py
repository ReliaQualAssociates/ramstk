# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.reliability.reliability_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Reliability module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKReliabilityRecord
from ramstk.models.dbtables import RAMSTKReliabilityTable

# noinspection PyUnresolvedReferences
from tests import MockDAO


@pytest.fixture(scope="function")
def test_table_model(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKReliabilityTable()
    dut.do_connect(mock_dao)

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


@pytest.mark.usefixtures("test_record_model", "test_table_model")
class TestCreateModels:
    """Class for testing model initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKReliabilityRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_reliability"
        assert test_record_model.hardware_id == 1
        assert test_record_model.add_adj_factor == 0.0
        assert test_record_model.availability_logistics == 1.0
        assert test_record_model.availability_mission == 1.0
        assert test_record_model.avail_log_variance == 0.0
        assert test_record_model.avail_mis_variance == 0.0
        assert test_record_model.failure_distribution_id == 0
        assert test_record_model.hazard_rate_active == 0.0
        assert test_record_model.hazard_rate_dormant == 0.0
        assert test_record_model.hazard_rate_logistics == 0.0
        assert test_record_model.hazard_rate_method_id == 0
        assert test_record_model.hazard_rate_mission == 0.0
        assert test_record_model.hazard_rate_model == ""
        assert test_record_model.hazard_rate_percent == 0.0
        assert test_record_model.hazard_rate_software == 0.0
        assert test_record_model.hazard_rate_specified == 0.0
        assert test_record_model.hazard_rate_type_id == 0
        assert test_record_model.hr_active_variance == 0.0
        assert test_record_model.hr_dormant_variance == 0.0
        assert test_record_model.hr_logistics_variance == 0.0
        assert test_record_model.hr_mission_variance == 0.0
        assert test_record_model.hr_specified_variance == 0.0
        assert test_record_model.location_parameter == 0.0
        assert test_record_model.mtbf_logistics == 0.0
        assert test_record_model.mtbf_mission == 0.0
        assert test_record_model.mtbf_specified == 0.0
        assert test_record_model.mtbf_logistics_variance == 0.0
        assert test_record_model.mtbf_mission_variance == 0.0
        assert test_record_model.mtbf_specified_variance == 0.0
        assert test_record_model.mult_adj_factor == 1.0
        assert test_record_model.quality_id == 0
        assert test_record_model.reliability_goal == 1.0
        assert test_record_model.reliability_goal_measure_id == 0
        assert test_record_model.reliability_logistics == 1.0
        assert test_record_model.reliability_mission == 1.0
        assert test_record_model.reliability_log_variance == 0.0
        assert test_record_model.reliability_miss_variance == 0.0
        assert test_record_model.scale_parameter == 0.0
        assert test_record_model.shape_parameter == 0.0
        assert test_record_model.survival_analysis_id == 0
        assert test_record_model.lambda_b == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_table_model):
        """should return a table manager instance."""
        assert isinstance(test_table_model, RAMSTKReliabilityTable)
        assert isinstance(test_table_model.tree, Tree)
        assert isinstance(test_table_model.dao, MockDAO)
        assert test_table_model._db_id_colname == "fld_hardware_id"
        assert test_table_model._db_tablename == "ramstk_reliability"
        assert test_table_model._select_msg == "selected_revision"
        assert test_table_model._root == 0
        assert test_table_model._tag == "reliability"
        assert test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
            "parent_id",
        ]
        assert test_table_model._revision_id == 0
        assert test_table_model._record == RAMSTKReliabilityRecord
        assert test_table_model.last_id == 0
        assert test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_table_model.do_get_attributes,
            "request_get_reliability_attributes",
        )
        assert pub.isSubscribed(
            test_table_model.do_set_attributes,
            "request_set_reliability_attributes",
        )
        assert pub.isSubscribed(
            test_table_model.do_set_attributes, "wvw_editing_reliability"
        )
        assert pub.isSubscribed(
            test_table_model.do_update_all, "request_update_all_reliability"
        )
        assert pub.isSubscribed(
            test_table_model.do_get_tree, "request_get_reliability_tree"
        )
        assert pub.isSubscribed(test_table_model.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_table_model.do_update, "request_update_reliability"
        )
        assert pub.isSubscribed(
            test_table_model.do_delete, "request_delete_reliability"
        )
        assert pub.isSubscribed(
            test_table_model.do_insert, "request_insert_reliability"
        )


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_table_model):
        """should return a record tree populated with DB records."""
        test_table_model.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_table_model.tree.get_node(1).data["reliability"],
            RAMSTKReliabilityRecord,
        )
        assert isinstance(
            test_table_model.tree.get_node(2).data["reliability"],
            RAMSTKReliabilityRecord,
        )
        assert isinstance(
            test_table_model.tree.get_node(3).data["reliability"],
            RAMSTKReliabilityRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_table_model):
        """should return the record for the passed record ID."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)

        assert isinstance(_reliability, RAMSTKReliabilityRecord)
        assert _reliability.revision_id == 1
        assert _reliability.hardware_id == 1
        assert _reliability.hazard_rate_active == 0.0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_table_model):
        """should return None when a non-existent record ID is requested."""
        test_table_model.do_select_all(attributes=test_attributes)

        assert test_table_model.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_table_model):
        """should return a new record instance with ID fields populated."""
        test_table_model.do_select_all(attributes=test_attributes)
        _new_record = test_table_model.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKReliabilityRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_table_model):
        """should add a new record to the records tree and update last_id."""
        test_table_model.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_attributes["parent_id"] = 1
        test_table_model.do_insert(attributes=test_attributes)

        assert test_table_model.last_id == 4
        assert isinstance(
            test_table_model.tree.get_node(4).data["reliability"],
            RAMSTKReliabilityRecord,
        )
        assert test_table_model.tree.get_node(4).data["reliability"].revision_id == 1
        assert test_table_model.tree.get_node(4).data["reliability"].hardware_id == 4


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_table_model):
        """should remove the record from the record tree and update last_id."""
        test_table_model.do_select_all(attributes=test_attributes)
        _last_id = test_table_model.last_id
        test_table_model.do_delete(node_id=_last_id)

        assert test_table_model.last_id == 2
        assert test_table_model.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["add_adj_factor"] == 0.0
        assert _attributes["availability_logistics"] == 1.0
        assert _attributes["availability_mission"] == 1.0
        assert _attributes["avail_log_variance"] == 0.0
        assert _attributes["avail_mis_variance"] == 0.0
        assert _attributes["failure_distribution_id"] == 0
        assert _attributes["hazard_rate_active"] == 0.0
        assert _attributes["hazard_rate_dormant"] == 0.0
        assert _attributes["hazard_rate_logistics"] == 0.0
        assert _attributes["hazard_rate_method_id"] == 0
        assert _attributes["hazard_rate_mission"] == 0.0
        assert _attributes["hazard_rate_model"] == ""
        assert _attributes["hazard_rate_percent"] == 0.0
        assert _attributes["hazard_rate_software"] == 0.0
        assert _attributes["hazard_rate_specified"] == 0.0
        assert _attributes["hazard_rate_type_id"] == 0
        assert _attributes["hr_active_variance"] == 0.0
        assert _attributes["hr_dormant_variance"] == 0.0
        assert _attributes["hr_logistics_variance"] == 0.0
        assert _attributes["hr_mission_variance"] == 0.0
        assert _attributes["hr_specified_variance"] == 0.0
        assert _attributes["lambda_b"] == 0.0
        assert _attributes["location_parameter"] == 0.0
        assert _attributes["mtbf_logistics"] == 0.0
        assert _attributes["mtbf_mission"] == 0.0
        assert _attributes["mtbf_specified"] == 0.0
        assert _attributes["mtbf_logistics_variance"] == 0.0
        assert _attributes["mtbf_mission_variance"] == 0.0
        assert _attributes["mtbf_specified_variance"] == 0.0
        assert _attributes["mult_adj_factor"] == 1.0
        assert _attributes["quality_id"] == 0
        assert _attributes["reliability_goal"] == 1.0
        assert _attributes["reliability_goal_measure_id"] == 0
        assert _attributes["reliability_logistics"] == 1.0
        assert _attributes["reliability_mission"] == 1.0
        assert _attributes["reliability_log_variance"] == 0.0
        assert _attributes["reliability_miss_variance"] == 0.0
        assert _attributes["scale_parameter"] == 0.0
        assert _attributes["shape_parameter"] == 0.0
        assert _attributes["survival_analysis_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_record_model):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_record_model
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["mtbf_mission"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_record_model.set_attributes(test_attributes) is None
        assert test_record_model.get_attributes()["mtbf_mission"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_record_model
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_predicted(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_method_id = 2
        _reliability.hazard_rate_type_id = 1
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["hazard_rate_method_id"] = 2
        test_attributes["hazard_rate_type_id"] = 1
        test_attributes["category_id"] = 1
        test_attributes["subcategory_id"] = 1
        test_attributes["application_id"] = 2
        test_attributes["area"] = 0.5
        test_attributes["environment_active_id"] = 3
        test_attributes["family_id"] = 2
        test_attributes["feature_size"] = 0.8
        test_attributes["manufacturing_id"] = 1
        test_attributes["n_elements"] = 100
        test_attributes["n_active_pins"] = 32
        test_attributes["package_id"] = 1
        test_attributes["power_operating"] = 0.038
        test_attributes["technology_id"] = 1
        test_attributes["temperature_case"] = 48.3
        test_attributes["theta_jc"] = 125
        test_attributes["type_id"] = 1
        test_attributes["voltage_esd"] = 2000
        test_attributes["years_in_production"] = 3
        test_attributes["piE"] = 1.0
        test_attributes["piQ"] = 2.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["part"] = 1
        test_attributes["quantity"] = 1
        test_attributes["temperature_junction"] = 25.0

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)

        assert _reliability.hazard_rate_active == pytest.approx(0.08514244)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_predicted_per_hour(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_method_id = 2
        _reliability.hazard_rate_type_id = 1
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["hazard_rate_method_id"] = 2
        test_attributes["hazard_rate_type_id"] = 1
        test_attributes["category_id"] = 1
        test_attributes["subcategory_id"] = 1
        test_attributes["application_id"] = 2
        test_attributes["area"] = 0.5
        test_attributes["environment_active_id"] = 3
        test_attributes["family_id"] = 2
        test_attributes["feature_size"] = 0.8
        test_attributes["manufacturing_id"] = 1
        test_attributes["n_elements"] = 100
        test_attributes["n_active_pins"] = 32
        test_attributes["package_id"] = 1
        test_attributes["power_operating"] = 0.038
        test_attributes["technology_id"] = 1
        test_attributes["temperature_case"] = 48.3
        test_attributes["theta_jc"] = 125
        test_attributes["type_id"] = 1
        test_attributes["voltage_esd"] = 2000
        test_attributes["years_in_production"] = 3
        test_attributes["piE"] = 1.0
        test_attributes["piQ"] = 2.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["part"] = 1
        test_attributes["quantity"] = 1
        test_attributes["temperature_junction"] = 25.0

        _reliability.do_calculate_hazard_rate_active(1000000.0, test_attributes)

        assert _reliability.hazard_rate_active == pytest.approx(8.5142443e-08)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_predicted_assembly(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_method_id = 2
        _reliability.hazard_rate_type_id = 1
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["hazard_rate_method_id"] = 2
        test_attributes["hazard_rate_type_id"] = 1
        test_attributes["duty_cycle"] = 100.0
        test_attributes["part"] = 0
        test_attributes["quantity"] = 1

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)

        assert _reliability.hazard_rate_active == 0.0

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_specified_ht(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_specified = 0.0032
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)

        assert _reliability.hazard_rate_active == pytest.approx(0.0032)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_specified_mtbf(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate when MTBF is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 3
        _reliability.mtbf_specified = 12632.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)

        assert _reliability.hazard_rate_active == pytest.approx(7.9164028e-05)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_exponential(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate for the EXP."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 1
        _reliability.scale_parameter = 10000.0
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        # One-parameter EXP.
        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)
        assert _reliability.hazard_rate_active == pytest.approx(0.0001)

        # Two-parameter EXP.
        _reliability.failure_distribution_id = 2
        _reliability.scale_parameter = 1000.0
        _reliability.location_parameter = 56.0

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)
        assert _reliability.hazard_rate_active == pytest.approx(0.0009469697)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_lognormal(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate for the LOGN at time."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 3
        _reliability.scale_parameter = 33.65
        _reliability.shape_parameter = 0.9663
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        # Two-parameter LOGN.
        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes, time=4.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.6610467)

        # Three-parameter LOGN.
        _reliability.failure_distribution_id = 4
        _reliability.location_parameter = 1.85

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes, time=4.0)
        assert _reliability.hazard_rate_active == pytest.approx(1.5117773)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_normal(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate for the NORM at time."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 5
        _reliability.scale_parameter = 10.0
        _reliability.shape_parameter = 0.0
        _reliability.location_parameter = 100.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        # Two-parameter NORM.
        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes, time=85.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.01387898)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_active_weibull(
        self, test_attributes, test_table_model
    ):
        """should calculate the active hazard rate for the WEI at time."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 4
        _reliability.failure_distribution_id = 6
        _reliability.scale_parameter = 525.0
        _reliability.shape_parameter = 2.5
        _reliability.location_parameter = 0.0
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        # Two-parameter WEI.
        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes, time=105.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.0235972)

        # Three-parameter WEI.
        _reliability.failure_distribution_id = 7
        _reliability.location_parameter = 18.5
        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes, time=105.0)
        assert _reliability.hazard_rate_active == pytest.approx(0.02874279)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_no_type(self, test_attributes, test_table_model):
        """should return zero for the active hazard rate when unknown type ID."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 5
        _reliability.hazard_rate_specified = 0.0032
        _reliability.add_adj_factor = 0.0
        _reliability.mult_adj_factor = 1.0
        test_attributes["duty_cycle"] = 100.0
        test_attributes["quantity"] = 1

        _reliability.do_calculate_hazard_rate_active(1.0, test_attributes)

        assert _reliability.hazard_rate_active == 0.0

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_logistics(
        self, test_attributes, test_table_model
    ):
        """should calculate the logistics hazard rate."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_active = 0.0032
        _reliability.hazard_rate_dormant = 0.000128
        _reliability.hazard_rate_software = 0.00005

        _reliability.do_calculate_hazard_rate_logistics()

        assert _reliability.hazard_rate_logistics == pytest.approx(0.003378)

    @pytest.mark.unit
    def test_do_calculate_hazard_rate_mission(self, test_attributes, test_table_model):
        """should calculate the mission hazard rate."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_active = 0.0032
        _reliability.hazard_rate_dormant = 0.000128
        _reliability.hazard_rate_software = 0.00005

        _reliability.do_calculate_hazard_rate_mission(0.55)

        assert _reliability.hazard_rate_mission == pytest.approx(0.0018676)

    @pytest.mark.unit
    def test_do_calculate_mtbf(self, test_attributes, test_table_model):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 3.378
        _reliability.hazard_rate_mission = 1.8676

        _reliability.do_calculate_mtbf()

        assert _reliability.mtbf_logistics == pytest.approx(296033.15571)
        assert _reliability.mtbf_mission == pytest.approx(535446.56243)

    @pytest.mark.unit
    def test_do_calculate_mtbf_per_hour(self, test_attributes, test_table_model):
        """should calculate the active hazard rate when hazard rate is specified."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 0.000003378
        _reliability.hazard_rate_mission = 0.0000018676

        _reliability.do_calculate_mtbf(multiplier=1000000.0)

        assert _reliability.mtbf_logistics == pytest.approx(296033.15571)
        assert _reliability.mtbf_mission == pytest.approx(535446.56243)

    @pytest.mark.unit
    def test_do_calculate_mtbf_zero_logistics(self, test_attributes, test_table_model):
        """should return 0.0 when the logistics hazard rate = 0.0."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 0.0
        _reliability.hazard_rate_mission = 1.8676

        _reliability.do_calculate_mtbf()

        assert _reliability.mtbf_logistics == 0.0
        assert _reliability.mtbf_mission == pytest.approx(535446.56243)

    @pytest.mark.unit
    def test_do_calculate_mtbf_zero_mission(self, test_attributes, test_table_model):
        """should return 0.0 when the logistics hazard rate = 0.0."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_logistics = 3.378
        _reliability.hazard_rate_mission = 0.0

        _reliability.do_calculate_mtbf()

        assert _reliability.mtbf_logistics == pytest.approx(296033.15571)
        assert _reliability.mtbf_mission == 0.0

    @pytest.mark.unit
    def test_do_calculate_reliability(self, test_attributes, test_table_model):
        """should calculate the active hazard rate for the EXP."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_logistics = 3.378
        _reliability.hazard_rate_mission = 1.8676

        _reliability.do_calculate_reliability(1.0)
        assert _reliability.reliability_logistics == pytest.approx(0.9999966)
        assert _reliability.reliability_mission == pytest.approx(0.9999981)

    @pytest.mark.unit
    def test_do_calculate_reliability_per_hour(self, test_attributes, test_table_model):
        """should calculate the active hazard rate for the EXP."""
        test_table_model.do_select_all(attributes=test_attributes)

        _reliability = test_table_model.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_logistics = 0.000003378
        _reliability.hazard_rate_mission = 0.0000018676

        _reliability.do_calculate_reliability(1.0, multiplier=1000000.0)
        assert _reliability.reliability_logistics == pytest.approx(0.9999966)
        assert _reliability.reliability_mission == pytest.approx(0.9999981)
