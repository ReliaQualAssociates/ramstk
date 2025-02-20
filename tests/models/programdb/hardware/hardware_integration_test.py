# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.hardware.hardware_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module integrations."""

# Standard Library Imports
from time import sleep

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKDesignElectricRecord,
    RAMSTKDesignMechanicRecord,
    RAMSTKHardwareRecord,
    RAMSTKMilHdbk217FRecord,
    RAMSTKNSWCRecord,
    RAMSTKReliabilityRecord,
)
from ramstk.models.dbtables import RAMSTKHardwareTable
from ramstk.models.dbviews import RAMSTKHardwareBoMView
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
    SystemTestUpdateMethods,
)


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_hardware")
    pub.unsubscribe(dut.do_update, "request_update_hardware")
    pub.unsubscribe(dut.do_get_tree, "request_get_hardware_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_hardware")
    pub.unsubscribe(dut.do_insert, "request_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_viewmodel():
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareBoMView()
    sleep(1)
    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_reliability")
    pub.unsubscribe(dut.do_calculate_hardware, "request_calculate_hardware")
    pub.unsubscribe(dut.do_make_composite_ref_des, "request_make_comp_ref_des")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectHardware(SystemTestSelectMethods):
    """Class for testing Hardware table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKHardwareRecord
    _select_id = 1
    _tag = "hardware"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertHardware(SystemTestInsertMethods):
    """Class for testing Hardware table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKHardwareRecord
    _tag = "hardware"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteHardware(SystemTestDeleteMethods):
    """Class for testing Hardware table do_delete() method."""

    __test__ = True

    _delete_id = 1
    _next_id = 0
    _record = RAMSTKHardwareRecord
    _tag = "hardware"


@pytest.mark.usefixtures(
    "test_tablemodel",
    "test_suite_logger",
)
class TestUpdateHardware(SystemTestUpdateMethods):
    """Class for testing Hardware table update() and update_all() methods."""

    __test__ = True

    _record = RAMSTKHardwareRecord
    _tag = "hardware"
    _update_bad_value_obj = {1: 2}
    _update_field_str = "specification_number"
    _update_id = 2
    _update_value_obj = "Big Specification"

    @pytest.mark.xfail(message="Unexpected failure occurs.")
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Test fails; does not pop record object."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterHardware(SystemTestGetterSetterMethods):
    """Class for testing Hardware table getter and setter methods."""

    __test__ = True

    _package = {"cage_code": "DE34T1"}
    _record = RAMSTKHardwareRecord
    _tag = "hardware"
    _test_id = 8


@pytest.mark.usefixtures(
    "test_attributes",
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
    "test_suite_logger",
)
class TestSelectHardwareBoM:
    """Class for testing Hardware BoM select_all() and select() methods."""

    def on_succeed_on_select_all(self, tree):
        """Listen for succeed_retrieve messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(8).data["hardware"], RAMSTKHardwareRecord)
        assert isinstance(
            tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            tree.get_node(8).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(tree.get_node(8).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        assert isinstance(tree.get_node(8).data["nswc"], RAMSTKNSWCRecord)
        assert isinstance(tree.get_node(8).data["reliability"], RAMSTKReliabilityRecord)
        print("\033[36m\n\tsucceed_retrieve_hardware_bom topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should return records tree with hardware tables."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_viewmodel.tree.get_node(8).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["reliability"],
            RAMSTKReliabilityRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(2).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(2).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should clear existing nodes from the records tree and then re-populate."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 8}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 8}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 8})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 8})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 8})

        assert isinstance(
            test_viewmodel.tree.get_node(8).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

        test_viewmodel.on_select_all()

        assert isinstance(
            test_viewmodel.tree.get_node(8).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should return an empty records tree if the base tree is empty."""
        test_viewmodel._dic_trees["hardware"] = Tree()

        assert test_viewmodel.on_select_all() is None
        assert test_viewmodel.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_attributes",
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
    "test_suite_logger",
)
class TestInsertHardwareBoM:
    """Class for testing the Hardware BoM insert() method."""

    def on_succeed_insert_hardware(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert tree.contains(10)
        print(
            "\033[36m\n\tsucceed_insert_hardware topic was broadcast on hardware "
            "insert."
        )

    @pytest.mark.skip
    def test_do_insert_hardware(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should add a new hardware record to the view model records tree."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert not test_viewmodel.tree.contains(10)

        pub.subscribe(self.on_succeed_insert_hardware, "succeed_retrieve_hardware_bom")

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "parent_id": 0,
                "part": 0,
            },
        )

        pub.unsubscribe(
            self.on_succeed_insert_hardware, "succeed_retrieve_hardware_bom"
        )


@pytest.mark.usefixtures(
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
    "test_suite_logger",
)
class TestDeleteHardwareBoM:
    """Class for testing the Hardware BoM do_delete() method."""

    def on_succeed_delete_hardware(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert not tree.contains(5)
        print(
            "\033[36m\n\tsucceed_retrieve_hardware_bom topic was broadcast on hardware "
            "delete."
        )

    @pytest.mark.skip
    def test_do_delete_hardware(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should remove deleted hardware from records tree."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert test_viewmodel.tree.contains(5)

        pub.subscribe(self.on_succeed_delete_hardware, "succeed_retrieve_hardware_bom")

        pub.sendMessage("request_delete_hardware", node_id=5)

        pub.unsubscribe(
            self.on_succeed_delete_hardware, "succeed_retrieve_hardware_bom"
        )


@pytest.mark.usefixtures(
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_electric",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
    "test_toml_user_configuration",
    "test_suite_logger",
)
class TestHardwareBoMAnalyses:
    """Class for testing Hardware BoM analytical methods."""

    @pytest.mark.integration
    def test_do_calculate_power_dissipation_part(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should calculate the total power dissipation of a part."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.part = 1
        _hardware.quantity = 2

        _design_electric = test_design_electric.do_select(8)
        _design_electric.power_operating = 0.00295

        test_viewmodel.do_calculate_power_dissipation(8)
        _attributes = test_tablemodel.do_select(8).get_attributes()

        assert _attributes["total_power_dissipation"] == 0.0059

    @pytest.mark.skip
    @pytest.mark.integration
    def test_do_calculate_power_dissipation_assembly(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Should calculate the total power dissipation of an assembly."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(2)
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(6)
        _hardware.part = 0
        _hardware.quantity = 4
        _hardware = test_tablemodel.do_select(7)
        _hardware.part = 1
        _hardware.quantity = 3

        _design_electric = test_design_electric.do_select(7)
        _design_electric.power_operating = 0.00295

        test_viewmodel.do_calculate_power_dissipation(2)
        _attributes = test_tablemodel.do_select(2).get_attributes()

        assert _attributes["total_power_dissipation"] == 0.00885

    @pytest.mark.integration
    def test_do_calculate_part_stress(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_stress_limits,
    ):
        """Calculate part stress ratios and check derating limits."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.subcategory_id = 2

        _hardware = test_reliability.do_select(8)
        _hardware.quality_id = 3

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 3
        _hardware.power_operating = 0.03
        _hardware.power_rated = 0.1
        _hardware.temperature_case = 46.9
        _hardware.temperature_knee = 85.0
        _hardware.temperature_rated_max = 150.0
        _hardware.voltage_operating = 3.3
        _hardware.voltage_rated = 5.0

        test_viewmodel._dic_stress_limits = test_stress_limits
        test_viewmodel.do_calculate_part_stress(8)

        assert _hardware.overstress == 0
        assert _hardware.reason == ""

    @pytest.mark.integration
    def test_do_calculate_part_stress_meter(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_stress_limits,
    ):
        """Calculate part stress ratios for meters."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 9
        _hardware.subcategory_id = 2

        _hardware = test_reliability.do_select(8)
        _hardware.quality_id = 3

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 3
        _hardware.power_operating = 0.03
        _hardware.power_rated = 0.1
        _hardware.temperature_case = 46.9
        _hardware.temperature_knee = 85.0
        _hardware.temperature_rated_max = 150.0
        _hardware.voltage_operating = 3.3
        _hardware.voltage_rated = 5.0

        test_viewmodel._dic_stress_limits = test_stress_limits
        test_viewmodel.do_calculate_part_stress(8)

        assert _hardware.overstress == 0
        assert _hardware.reason == ""

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_mil_hdbk_217f(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_stress_limits,
    ):
        """Predict the active hazard of a part using MIL-HDBK-217F."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.subcategory_id = 1
        _hardware.part = 1

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 9

        _hardware = test_milhdbk217f.do_select(8)
        _hardware.piR = 0.0038

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 1
        _hardware.hazard_rate_method_id = 2
        _hardware.quality_id = 3

        test_viewmodel._dic_stress_limits = test_stress_limits
        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(0.003995836)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_specified_hazard_rate(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Predict the active hazard of an assembly with specified hazard rate.."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.000007829

        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(7.829e-06)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_specified_mtbf(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Predict the active hazard of an assembly with specified MTBF."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 3
        _hardware.mtbf_specified = 127730.0

        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(7.8290143e-06)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_assessed(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_toml_user_configuration,
    ):
        """Predict the active hazard of an assembly by sum of children."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        test_design_electric._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )

        _hardware = test_tablemodel.do_select(1)
        _hardware.quantity = 1
        _hardware.part = 0

        _hardware = test_reliability.do_select(1)
        _hardware.hazard_rate_type_id = 1

        _hardware = test_tablemodel.do_select(2)
        _hardware.quantity = 2
        _hardware.part = 0

        _hardware = test_reliability.do_select(2)
        _hardware.hazard_rate_type_id = 1

        for _id in [3, 4, 5, 6, 7]:
            _hardware = test_tablemodel.do_select(_id)
            _hardware.quantity = 1
            _hardware.part = 0

            _hardware = test_reliability.do_select(_id)
            _hardware.hazard_rate_type_id = 2
            _hardware.hazard_rate_specified = 0.0001 * (_id - 2)

        _hardware = test_reliability.do_select(7)
        _hardware.hazard_rate_type_id = 1

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.000004815

        test_viewmodel.do_calculate_hardware(1)

        _attributes = test_reliability.do_select(8).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.000004815)

        _attributes = test_reliability.do_select(7).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.000004815)

        _attributes = test_reliability.do_select(6).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0004)

        _attributes = test_reliability.do_select(5).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0003)

        _attributes = test_reliability.do_select(4).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0002)

        _attributes = test_reliability.do_select(3).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0001)

        _attributes = test_reliability.do_select(2).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00080963)

        _attributes = test_reliability.do_select(1).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00140963)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_specified_hazard_rate(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Predict the active hazard of an assembly with specified hazard rate."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(5)
        _hardware.quantity = 1
        _hardware.part = 0

        _hardware = test_reliability.do_select(5)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.0007829

        test_viewmodel.do_calculate_hardware(5)

        _attributes = test_reliability.do_select(5).get_attributes()
        assert _attributes["hazard_rate_active"] == 0.0007829

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_specified_mtbf(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """Predict the active hazard of an assembly with specified MTBF."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(2)
        _hardware.quantity = 3
        _hardware.part = 0

        _hardware = test_reliability.do_select(2)
        _hardware.hazard_rate_type_id = 3
        _hardware.mtbf_specified = 10000.0

        test_viewmodel.do_calculate_hardware(2)
        _attributes = test_reliability.do_select(2).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(0.0003)

    @pytest.mark.integration
    def test_do_calculate_hardware(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_toml_user_configuration,
    ):
        """Calculate all hardware metrics for a part."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        test_design_electric._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.cost = 12.98
        _hardware.cost_type_id = 2
        _hardware.part = 1
        _hardware.quantity = 2
        _hardware.subcategory_id = 1

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 9
        _hardware.environment_dormant_id = 1
        _hardware.power_operating = 0.00295

        _hardware = test_milhdbk217f.do_select(8)
        _hardware.piR = 0.0038

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 1
        _hardware.hazard_rate_method_id = 1
        _hardware.quality_id = 3

        test_viewmodel.do_calculate_hardware(8)

        _attributes = test_tablemodel.do_select(8).get_attributes()
        assert _attributes["total_cost"] == 25.96
        assert _attributes["total_part_count"] == 2
        assert _attributes["total_power_dissipation"] == 0.0059

        _attributes = test_reliability.do_select(8).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.015)
        assert _attributes["hazard_rate_dormant"] == pytest.approx(0.00045)
        assert _attributes["hazard_rate_logistics"] == pytest.approx(0.01545)
        assert _attributes["hazard_rate_mission"] == pytest.approx(1.45545)
        assert _attributes["mtbf_logistics"] == pytest.approx(64724919.0938511)
        assert _attributes["mtbf_mission"] == pytest.approx(687072.7266481)
        assert _attributes["reliability_logistics"] == pytest.approx(0.9999985)
        assert _attributes["reliability_mission"] == pytest.approx(0.9998545)
