# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKReliabilityRecord


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _reliability_1 = RAMSTKReliabilityRecord()
    _reliability_1.revision_id = 1
    _reliability_1.hardware_id = 1
    _reliability_1.add_adj_factor = 0.0
    _reliability_1.availability_logistics = 1.0
    _reliability_1.availability_mission = 1.0
    _reliability_1.avail_log_variance = 0.0
    _reliability_1.avail_mis_variance = 0.0
    _reliability_1.failure_distribution_id = 0
    _reliability_1.hazard_rate_active = 0.0
    _reliability_1.hazard_rate_dormant = 0.0
    _reliability_1.hazard_rate_logistics = 0.0
    _reliability_1.hazard_rate_method_id = 0
    _reliability_1.hazard_rate_mission = 0.0
    _reliability_1.hazard_rate_model = ""
    _reliability_1.hazard_rate_percent = 0.0
    _reliability_1.hazard_rate_software = 0.0
    _reliability_1.hazard_rate_specified = 0.0
    _reliability_1.hazard_rate_type_id = 0
    _reliability_1.hr_active_variance = 0.0
    _reliability_1.hr_dormant_variance = 0.0
    _reliability_1.hr_logistics_variance = 0.0
    _reliability_1.hr_mission_variance = 0.0
    _reliability_1.hr_specified_variance = 0.0
    _reliability_1.lambda_b = 0.0
    _reliability_1.location_parameter = 0.0
    _reliability_1.mtbf_logistics = 0.0
    _reliability_1.mtbf_mission = 0.0
    _reliability_1.mtbf_specified = 0.0
    _reliability_1.mtbf_logistics_variance = 0.0
    _reliability_1.mtbf_mission_variance = 0.0
    _reliability_1.mtbf_specified_variance = 0.0
    _reliability_1.mult_adj_factor = 1.0
    _reliability_1.quality_id = 0
    _reliability_1.reliability_goal = 1.0
    _reliability_1.reliability_goal_measure_id = 0
    _reliability_1.reliability_logistics = 1.0
    _reliability_1.reliability_mission = 1.0
    _reliability_1.reliability_log_variance = 0.0
    _reliability_1.reliability_miss_variance = 0.0
    _reliability_1.scale_parameter = 0.0
    _reliability_1.shape_parameter = 0.0
    _reliability_1.survival_analysis_id = 0

    _reliability_2 = RAMSTKReliabilityRecord()
    _reliability_2.revision_id = 1
    _reliability_2.hardware_id = 2
    _reliability_2.add_adj_factor = 0.0
    _reliability_2.availability_logistics = 1.0
    _reliability_2.availability_mission = 1.0
    _reliability_2.avail_log_variance = 0.0
    _reliability_2.avail_mis_variance = 0.0
    _reliability_2.failure_distribution_id = 0
    _reliability_2.hazard_rate_active = 0.0
    _reliability_2.hazard_rate_dormant = 0.0
    _reliability_2.hazard_rate_logistics = 0.0
    _reliability_2.hazard_rate_method_id = 0
    _reliability_2.hazard_rate_mission = 0.0
    _reliability_2.hazard_rate_model = ""
    _reliability_2.hazard_rate_percent = 0.0
    _reliability_2.hazard_rate_software = 0.0
    _reliability_2.hazard_rate_specified = 0.0
    _reliability_2.hazard_rate_type_id = 0
    _reliability_2.hr_active_variance = 0.0
    _reliability_2.hr_dormant_variance = 0.0
    _reliability_2.hr_logistics_variance = 0.0
    _reliability_2.hr_mission_variance = 0.0
    _reliability_2.hr_specified_variance = 0.0
    _reliability_2.lambda_b = 0.0
    _reliability_2.location_parameter = 0.0
    _reliability_2.mtbf_logistics = 0.0
    _reliability_2.mtbf_mission = 0.0
    _reliability_2.mtbf_specified = 0.0
    _reliability_2.mtbf_logistics_variance = 0.0
    _reliability_2.mtbf_mission_variance = 0.0
    _reliability_2.mtbf_specified_variance = 0.0
    _reliability_2.mult_adj_factor = 1.0
    _reliability_2.quality_id = 0
    _reliability_2.reliability_goal = 1.0
    _reliability_2.reliability_goal_measure_id = 0
    _reliability_2.reliability_logistics = 1.0
    _reliability_2.reliability_mission = 1.0
    _reliability_2.reliability_log_variance = 0.0
    _reliability_2.reliability_miss_variance = 0.0
    _reliability_2.scale_parameter = 0.0
    _reliability_2.shape_parameter = 0.0
    _reliability_2.survival_analysis_id = 0

    _reliability_3 = RAMSTKReliabilityRecord()
    _reliability_3.revision_id = 1
    _reliability_3.hardware_id = 3
    _reliability_3.add_adj_factor = 0.0
    _reliability_3.availability_logistics = 1.0
    _reliability_3.availability_mission = 1.0
    _reliability_3.avail_log_variance = 0.0
    _reliability_3.avail_mis_variance = 0.0
    _reliability_3.failure_distribution_id = 0
    _reliability_3.hazard_rate_active = 0.0
    _reliability_3.hazard_rate_dormant = 0.0
    _reliability_3.hazard_rate_logistics = 0.0
    _reliability_3.hazard_rate_method_id = 0
    _reliability_3.hazard_rate_mission = 0.0
    _reliability_3.hazard_rate_model = ""
    _reliability_3.hazard_rate_percent = 0.0
    _reliability_3.hazard_rate_software = 0.0
    _reliability_3.hazard_rate_specified = 0.0
    _reliability_3.hazard_rate_type_id = 0
    _reliability_3.hr_active_variance = 0.0
    _reliability_3.hr_dormant_variance = 0.0
    _reliability_3.hr_logistics_variance = 0.0
    _reliability_3.hr_mission_variance = 0.0
    _reliability_3.hr_specified_variance = 0.0
    _reliability_3.lambda_b = 0.0
    _reliability_3.location_parameter = 0.0
    _reliability_3.mtbf_logistics = 0.0
    _reliability_3.mtbf_mission = 0.0
    _reliability_3.mtbf_specified = 0.0
    _reliability_3.mtbf_logistics_variance = 0.0
    _reliability_3.mtbf_mission_variance = 0.0
    _reliability_3.mtbf_specified_variance = 0.0
    _reliability_3.mult_adj_factor = 1.0
    _reliability_3.quality_id = 0
    _reliability_3.reliability_goal = 1.0
    _reliability_3.reliability_goal_measure_id = 0
    _reliability_3.reliability_logistics = 1.0
    _reliability_3.reliability_mission = 1.0
    _reliability_3.reliability_log_variance = 0.0
    _reliability_3.reliability_miss_variance = 0.0
    _reliability_3.scale_parameter = 0.0
    _reliability_3.shape_parameter = 0.0
    _reliability_3.survival_analysis_id = 0

    DAO = MockDAO()
    DAO.table = [
        _reliability_1,
        _reliability_2,
        _reliability_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "add_adj_factor": 0.0,
        "availability_logistics": 1.0,
        "availability_mission": 1.0,
        "avail_log_variance": 0.0,
        "avail_mis_variance": 0.0,
        "failure_distribution_id": 0,
        "hazard_rate_active": 0.0,
        "hazard_rate_dormant": 0.0,
        "hazard_rate_logistics": 0.0,
        "hazard_rate_method_id": 0,
        "hazard_rate_mission": 0.0,
        "hazard_rate_model": "",
        "hazard_rate_percent": 0.0,
        "hazard_rate_software": 0.0,
        "hazard_rate_specified": 0.0,
        "hazard_rate_type_id": 0,
        "hr_active_variance": 0.0,
        "hr_dormant_variance": 0.0,
        "hr_logistics_variance": 0.0,
        "hr_mission_variance": 0.0,
        "hr_specified_variance": 0.0,
        "lambda_b": 0.0,
        "location_parameter": 0.0,
        "mtbf_logistics": 0.0,
        "mtbf_mission": 0.0,
        "mtbf_specified": 0.0,
        "mtbf_logistics_variance": 0.0,
        "mtbf_mission_variance": 0.0,
        "mtbf_specified_variance": 0.0,
        "mult_adj_factor": 1.0,
        "quality_id": 0,
        "reliability_goal": 1.0,
        "reliability_goal_measure_id": 0,
        "reliability_logistics": 1.0,
        "reliability_mission": 1.0,
        "reliability_log_variance": 0.0,
        "reliability_miss_variance": 0.0,
        "scale_parameter": 0.0,
        "shape_parameter": 0.0,
        "survival_analysis_id": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKReliabilityRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
