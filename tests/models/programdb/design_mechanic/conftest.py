# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKDesignMechanicRecord


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _design_mechanic_1 = RAMSTKDesignMechanicRecord()
    _design_mechanic_1.revision_id = 1
    _design_mechanic_1.hardware_id = 1
    _design_mechanic_1.altitude_operating = 0.0
    _design_mechanic_1.application_id = 0
    _design_mechanic_1.balance_id = 0
    _design_mechanic_1.clearance = 0.0
    _design_mechanic_1.casing_id = 0
    _design_mechanic_1.contact_pressure = 0.0
    _design_mechanic_1.deflection = 0.0
    _design_mechanic_1.diameter_coil = 0.0
    _design_mechanic_1.diameter_inner = 0.0
    _design_mechanic_1.diameter_outer = 0.0
    _design_mechanic_1.diameter_wire = 0.0
    _design_mechanic_1.filter_size = 0.0
    _design_mechanic_1.flow_design = 0.0
    _design_mechanic_1.flow_operating = 0.0
    _design_mechanic_1.frequency_operating = 0.0
    _design_mechanic_1.friction = 0.0
    _design_mechanic_1.impact_id = 0
    _design_mechanic_1.leakage_allowable = 0.0
    _design_mechanic_1.length = 0.0
    _design_mechanic_1.length_compressed = 0.0
    _design_mechanic_1.length_relaxed = 0.0
    _design_mechanic_1.load_design = 0.0
    _design_mechanic_1.load_id = 0
    _design_mechanic_1.load_operating = 0.0
    _design_mechanic_1.lubrication_id = 0
    _design_mechanic_1.manufacturing_id = 0
    _design_mechanic_1.material_id = 0
    _design_mechanic_1.meyer_hardness = 0.0
    _design_mechanic_1.misalignment_angle = 0.0
    _design_mechanic_1.n_ten = 0
    _design_mechanic_1.n_cycles = 0
    _design_mechanic_1.n_elements = 0
    _design_mechanic_1.offset = 0.0
    _design_mechanic_1.particle_size = 0.0
    _design_mechanic_1.pressure_contact = 0.0
    _design_mechanic_1.pressure_delta = 0.0
    _design_mechanic_1.pressure_downstream = 0.0
    _design_mechanic_1.pressure_rated = 0.0
    _design_mechanic_1.pressure_upstream = 0.0
    _design_mechanic_1.rpm_design = 0.0
    _design_mechanic_1.rpm_operating = 0.0
    _design_mechanic_1.service_id = 0
    _design_mechanic_1.spring_index = 0.0
    _design_mechanic_1.surface_finish = 0.0
    _design_mechanic_1.technology_id = 0
    _design_mechanic_1.thickness = 0.0
    _design_mechanic_1.torque_id = 0
    _design_mechanic_1.type_id = 0
    _design_mechanic_1.viscosity_design = 0.0
    _design_mechanic_1.viscosity_dynamic = 0.0
    _design_mechanic_1.water_per_cent = 0.0
    _design_mechanic_1.width_minimum = 0.0

    _design_mechanic_2 = RAMSTKDesignMechanicRecord()
    _design_mechanic_2.revision_id = 1
    _design_mechanic_2.hardware_id = 2
    _design_mechanic_2.altitude_operating = 0.0
    _design_mechanic_2.application_id = 0
    _design_mechanic_2.balance_id = 0
    _design_mechanic_2.clearance = 0.0
    _design_mechanic_2.casing_id = 0
    _design_mechanic_2.contact_pressure = 0.0
    _design_mechanic_2.deflection = 0.0
    _design_mechanic_2.diameter_coil = 0.0
    _design_mechanic_2.diameter_inner = 0.0
    _design_mechanic_2.diameter_outer = 0.0
    _design_mechanic_2.diameter_wire = 0.0
    _design_mechanic_2.filter_size = 0.0
    _design_mechanic_2.flow_design = 0.0
    _design_mechanic_2.flow_operating = 0.0
    _design_mechanic_2.frequency_operating = 0.0
    _design_mechanic_2.friction = 0.0
    _design_mechanic_2.impact_id = 0
    _design_mechanic_2.leakage_allowable = 0.0
    _design_mechanic_2.length = 0.0
    _design_mechanic_2.length_compressed = 0.0
    _design_mechanic_2.length_relaxed = 0.0
    _design_mechanic_2.load_design = 0.0
    _design_mechanic_2.load_id = 0
    _design_mechanic_2.load_operating = 0.0
    _design_mechanic_2.lubrication_id = 0
    _design_mechanic_2.manufacturing_id = 0
    _design_mechanic_2.material_id = 0
    _design_mechanic_2.meyer_hardness = 0.0
    _design_mechanic_2.misalignment_angle = 0.0
    _design_mechanic_2.n_ten = 0
    _design_mechanic_2.n_cycles = 0
    _design_mechanic_2.n_elements = 0
    _design_mechanic_2.offset = 0.0
    _design_mechanic_2.particle_size = 0.0
    _design_mechanic_2.pressure_contact = 0.0
    _design_mechanic_2.pressure_delta = 0.0
    _design_mechanic_2.pressure_downstream = 0.0
    _design_mechanic_2.pressure_rated = 0.0
    _design_mechanic_2.pressure_upstream = 0.0
    _design_mechanic_2.rpm_design = 0.0
    _design_mechanic_2.rpm_operating = 0.0
    _design_mechanic_2.service_id = 0
    _design_mechanic_2.spring_index = 0.0
    _design_mechanic_2.surface_finish = 0.0
    _design_mechanic_2.technology_id = 0
    _design_mechanic_2.thickness = 0.0
    _design_mechanic_2.torque_id = 0
    _design_mechanic_2.type_id = 0
    _design_mechanic_2.viscosity_design = 0.0
    _design_mechanic_2.viscosity_dynamic = 0.0
    _design_mechanic_2.water_per_cent = 0.0
    _design_mechanic_2.width_minimum = 0.0

    _design_mechanic_3 = RAMSTKDesignMechanicRecord()
    _design_mechanic_3.revision_id = 1
    _design_mechanic_3.hardware_id = 3
    _design_mechanic_3.altitude_operating = 0.0
    _design_mechanic_3.application_id = 0
    _design_mechanic_3.balance_id = 0
    _design_mechanic_3.clearance = 0.0
    _design_mechanic_3.casing_id = 0
    _design_mechanic_3.contact_pressure = 0.0
    _design_mechanic_3.deflection = 0.0
    _design_mechanic_3.diameter_coil = 0.0
    _design_mechanic_3.diameter_inner = 0.0
    _design_mechanic_3.diameter_outer = 0.0
    _design_mechanic_3.diameter_wire = 0.0
    _design_mechanic_3.filter_size = 0.0
    _design_mechanic_3.flow_design = 0.0
    _design_mechanic_3.flow_operating = 0.0
    _design_mechanic_3.frequency_operating = 0.0
    _design_mechanic_3.friction = 0.0
    _design_mechanic_3.impact_id = 0
    _design_mechanic_3.leakage_allowable = 0.0
    _design_mechanic_3.length = 0.0
    _design_mechanic_3.length_compressed = 0.0
    _design_mechanic_3.length_relaxed = 0.0
    _design_mechanic_3.load_design = 0.0
    _design_mechanic_3.load_id = 0
    _design_mechanic_3.load_operating = 0.0
    _design_mechanic_3.lubrication_id = 0
    _design_mechanic_3.manufacturing_id = 0
    _design_mechanic_3.material_id = 0
    _design_mechanic_3.meyer_hardness = 0.0
    _design_mechanic_3.misalignment_angle = 0.0
    _design_mechanic_3.n_ten = 0
    _design_mechanic_3.n_cycles = 0
    _design_mechanic_3.n_elements = 0
    _design_mechanic_3.offset = 0.0
    _design_mechanic_3.particle_size = 0.0
    _design_mechanic_3.pressure_contact = 0.0
    _design_mechanic_3.pressure_delta = 0.0
    _design_mechanic_3.pressure_downstream = 0.0
    _design_mechanic_3.pressure_rated = 0.0
    _design_mechanic_3.pressure_upstream = 0.0
    _design_mechanic_3.rpm_design = 0.0
    _design_mechanic_3.rpm_operating = 0.0
    _design_mechanic_3.service_id = 0
    _design_mechanic_3.spring_index = 0.0
    _design_mechanic_3.surface_finish = 0.0
    _design_mechanic_3.technology_id = 0
    _design_mechanic_3.thickness = 0.0
    _design_mechanic_3.torque_id = 0
    _design_mechanic_3.type_id = 0
    _design_mechanic_3.viscosity_design = 0.0
    _design_mechanic_3.viscosity_dynamic = 0.0
    _design_mechanic_3.water_per_cent = 0.0
    _design_mechanic_3.width_minimum = 0.0

    DAO = MockDAO()
    DAO.table = [
        _design_mechanic_1,
        _design_mechanic_2,
        _design_mechanic_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "altitude_operating": 0.0,
        "application_id": 0,
        "balance_id": 0,
        "clearance": 0.0,
        "casing_id": 0,
        "contact_pressure": 0.0,
        "deflection": 0.0,
        "diameter_coil": 0.0,
        "diameter_inner": 0.0,
        "diameter_outer": 0.0,
        "diameter_wire": 0.0,
        "filter_size": 0.0,
        "flow_design": 0.0,
        "flow_operating": 0.0,
        "frequency_operating": 0.0,
        "friction": 0.0,
        "impact_id": 0,
        "leakage_allowable": 0.0,
        "length": 0.0,
        "length_compressed": 0.0,
        "length_relaxed": 0.0,
        "load_design": 0.0,
        "load_id": 0,
        "load_operating": 0.0,
        "lubrication_id": 0,
        "manufacturing_id": 0,
        "material_id": 0,
        "meyer_hardness": 0.0,
        "misalignment_angle": 0.0,
        "n_ten": 0,
        "n_cycles": 0,
        "n_elements": 0,
        "offset": 0.0,
        "particle_size": 0.0,
        "pressure_contact": 0.0,
        "pressure_delta": 0.0,
        "pressure_downstream": 0.0,
        "pressure_rated": 0.0,
        "pressure_upstream": 0.0,
        "rpm_design": 0.0,
        "rpm_operating": 0.0,
        "service_id": 0,
        "spring_index": 0.0,
        "surface_finish": 0.0,
        "technology_id": 0,
        "thickness": 0.0,
        "torque_id": 0,
        "type_id": 0,
        "viscosity_design": 0.0,
        "viscosity_dynamic": 0.0,
        "water_per_cent": 0.0,
        "width_minimum": 0.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKDesignMechanicRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
