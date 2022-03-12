# Third Party Imports
import pytest


@pytest.fixture
def test_attributes_allocation():
    yield {
        "allocation_method_id": 1,
        "availability_alloc": 0.9998,
        "duty_cycle": 100.0,
        "env_factor": 6,
        "goal_measure_id": 1,
        "hazard_rate_alloc": 0.0,
        "hazard_rate_goal": 0.0,
        "included": 1,
        "int_factor": 3,
        "mission_time": 100.0,
        "mtbf_alloc": 0.0,
        "mtbf_goal": 0.0,
        "n_sub_systems": 3,
        "n_sub_elements": 3,
        "parent_id": 1,
        "percent_weight_factor": 0.8,
        "reliability_alloc": 0.99975,
        "reliability_goal": 0.999,
        "op_time_factor": 5,
        "soa_factor": 2,
        "weight_factor": 1,
    }
