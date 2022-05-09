# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.design_mechanic.design_mechanic_unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Mechanic module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKDesignMechanicRecord
from ramstk.models.dbtables import RAMSTKDesignMechanicTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateDesignMechanicModels:
    """Class for unit testing Design Mechanic model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return a Design Mechanic record model instance."""
        assert isinstance(test_record_model, RAMSTKDesignMechanicRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_design_mechanic"
        assert test_record_model.hardware_id == 1
        assert test_record_model.altitude_operating == 0.0
        assert test_record_model.application_id == 0
        assert test_record_model.balance_id == 0
        assert test_record_model.clearance == 0.0
        assert test_record_model.casing_id == 0
        assert test_record_model.contact_pressure == 0.0
        assert test_record_model.deflection == 0.0
        assert test_record_model.diameter_coil == 0.0
        assert test_record_model.diameter_inner == 0.0
        assert test_record_model.diameter_outer == 0.0
        assert test_record_model.diameter_wire == 0.0
        assert test_record_model.filter_size == 0.0
        assert test_record_model.flow_design == 0.0
        assert test_record_model.flow_operating == 0.0
        assert test_record_model.frequency_operating == 0.0
        assert test_record_model.friction == 0.0
        assert test_record_model.impact_id == 0
        assert test_record_model.leakage_allowable == 0.0
        assert test_record_model.length == 0.0
        assert test_record_model.length_compressed == 0.0
        assert test_record_model.length_relaxed == 0.0
        assert test_record_model.load_design == 0.0
        assert test_record_model.load_id == 0
        assert test_record_model.load_operating == 0.0
        assert test_record_model.lubrication_id == 0
        assert test_record_model.manufacturing_id == 0
        assert test_record_model.material_id == 0
        assert test_record_model.meyer_hardness == 0.0
        assert test_record_model.misalignment_angle == 0.0
        assert test_record_model.n_ten == 0
        assert test_record_model.n_cycles == 0
        assert test_record_model.n_elements == 0
        assert test_record_model.offset == 0.0
        assert test_record_model.particle_size == 0.0
        assert test_record_model.pressure_contact == 0.0
        assert test_record_model.pressure_delta == 0.0
        assert test_record_model.pressure_downstream == 0.0
        assert test_record_model.pressure_rated == 0.0
        assert test_record_model.pressure_upstream == 0.0
        assert test_record_model.rpm_design == 0.0
        assert test_record_model.rpm_operating == 0.0
        assert test_record_model.service_id == 0
        assert test_record_model.spring_index == 0.0
        assert test_record_model.surface_finish == 0.0
        assert test_record_model.technology_id == 0
        assert test_record_model.thickness == 0.0
        assert test_record_model.torque_id == 0
        assert test_record_model.type_id == 0
        assert test_record_model.viscosity_design == 0.0
        assert test_record_model.viscosity_dynamic == 0.0
        assert test_record_model.water_per_cent == 0.0
        assert test_record_model.width_minimum == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Design Mechanic table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKDesignMechanicTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_design_mechanic"
        assert unit_test_table_model._select_msg == "selected_revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._tag == "design_mechanic"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKDesignMechanicRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_design_mechanic_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_design_mechanic_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_design_mechanic"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_design_mechanic"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_design_mechanic_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_design_mechanic"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_design_mechanic"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_design_mechanic"
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree, "succeed_delete_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree, "succeed_insert_hardware"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectDesignMechanic(UnitTestSelectMethods):
    """Class for unit testing Design Mechanic table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertDesignMechanic(UnitTestInsertMethods):
    """Class for unit testing Design Mechanic table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"

    @pytest.mark.skip(reason="Design Mechanic records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Design Mechanic records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteDesignMechanic(UnitTestDeleteMethods):
    """Class for unit testing Design Mechanic table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterDesignMechanic(UnitTestGetterSetterMethods):
    """Class for unit testing Design Mechanic table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]
    _test_attr = "type_id"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["pressure_upstream"] == 0.0
        assert _attributes["frequency_operating"] == 0.0
        assert _attributes["surface_finish"] == 0.0
        assert _attributes["friction"] == 0.0
        assert _attributes["length_compressed"] == 0.0
        assert _attributes["load_id"] == 0
        assert _attributes["n_cycles"] == 0
        assert _attributes["balance_id"] == 0
        assert _attributes["lubrication_id"] == 0
        assert _attributes["water_per_cent"] == 0.0
        assert _attributes["misalignment_angle"] == 0.0
        assert _attributes["type_id"] == 0
        assert _attributes["rpm_design"] == 0.0
        assert _attributes["pressure_downstream"] == 0.0
        assert _attributes["diameter_coil"] == 0.0
        assert _attributes["manufacturing_id"] == 0
        assert _attributes["pressure_contact"] == 0.0
        assert _attributes["meyer_hardness"] == 0.0
        assert _attributes["rpm_operating"] == 0.0
        assert _attributes["length_relaxed"] == 0.0
        assert _attributes["impact_id"] == 0
        assert _attributes["n_ten"] == 0
        assert _attributes["material_id"] == 0
        assert _attributes["technology_id"] == 0
        assert _attributes["service_id"] == 0
        assert _attributes["flow_design"] == 0.0
        assert _attributes["application_id"] == 0
        assert _attributes["diameter_wire"] == 0.0
        assert _attributes["deflection"] == 0.0
        assert _attributes["filter_size"] == 0.0
        assert _attributes["diameter_inner"] == 0.0
        assert _attributes["pressure_rated"] == 0.0
        assert _attributes["hardware_id"] == 1
        assert _attributes["altitude_operating"] == 0.0
        assert _attributes["thickness"] == 0.0
        assert _attributes["diameter_outer"] == 0.0
        assert _attributes["n_elements"] == 0
        assert _attributes["contact_pressure"] == 0.0
        assert _attributes["particle_size"] == 0.0
        assert _attributes["casing_id"] == 0
        assert _attributes["viscosity_dynamic"] == 0.0
        assert _attributes["viscosity_design"] == 0.0
        assert _attributes["torque_id"] == 0
        assert _attributes["leakage_allowable"] == 0.0
        assert _attributes["offset"] == 0.0
        assert _attributes["width_minimum"] == 0.0
        assert _attributes["load_operating"] == 0.0
        assert _attributes["spring_index"] == 0.0
        assert _attributes["flow_operating"] == 0.0
        assert _attributes["pressure_delta"] == 0.0
        assert _attributes["length"] == 0.0
        assert _attributes["load_design"] == 0.0
        assert _attributes["clearance"] == 0.0
