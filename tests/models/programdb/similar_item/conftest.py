# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKSimilarItemRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _similar_item_1 = RAMSTKSimilarItemRecord()
    _similar_item_1.revision_id = 1
    _similar_item_1.hardware_id = 1
    _similar_item_1.change_description_1 = ""
    _similar_item_1.change_description_2 = ""
    _similar_item_1.change_description_3 = ""
    _similar_item_1.change_description_4 = ""
    _similar_item_1.change_description_5 = ""
    _similar_item_1.change_description_6 = ""
    _similar_item_1.change_description_7 = ""
    _similar_item_1.change_description_8 = ""
    _similar_item_1.change_description_9 = ""
    _similar_item_1.change_description_10 = ""
    _similar_item_1.change_factor_1 = 1.0
    _similar_item_1.change_factor_2 = 1.0
    _similar_item_1.change_factor_3 = 1.0
    _similar_item_1.change_factor_4 = 1.0
    _similar_item_1.change_factor_5 = 1.0
    _similar_item_1.change_factor_6 = 1.0
    _similar_item_1.change_factor_7 = 1.0
    _similar_item_1.change_factor_8 = 1.0
    _similar_item_1.change_factor_9 = 1.0
    _similar_item_1.change_factor_10 = 1.0
    _similar_item_1.environment_from_id = 0
    _similar_item_1.environment_to_id = 0
    _similar_item_1.function_1 = "0"
    _similar_item_1.function_2 = "0"
    _similar_item_1.function_3 = "0"
    _similar_item_1.function_4 = "0"
    _similar_item_1.function_5 = "0"
    _similar_item_1.parent_id = 0
    _similar_item_1.similar_item_method_id = 1
    _similar_item_1.quality_from_id = 0
    _similar_item_1.quality_to_id = 0
    _similar_item_1.result_1 = 0.0
    _similar_item_1.result_2 = 0.0
    _similar_item_1.result_3 = 0.0
    _similar_item_1.result_4 = 0.0
    _similar_item_1.result_5 = 0.0
    _similar_item_1.temperature_from = 30.0
    _similar_item_1.temperature_to = 30.0
    _similar_item_1.user_blob_1 = ""
    _similar_item_1.user_blob_2 = ""
    _similar_item_1.user_blob_3 = ""
    _similar_item_1.user_blob_4 = ""
    _similar_item_1.user_blob_5 = ""
    _similar_item_1.user_float_1 = 0.0
    _similar_item_1.user_float_2 = 0.0
    _similar_item_1.user_float_3 = 0.0
    _similar_item_1.user_float_4 = 0.0
    _similar_item_1.user_float_5 = 0.0
    _similar_item_1.user_int_1 = 0
    _similar_item_1.user_int_2 = 0
    _similar_item_1.user_int_3 = 0
    _similar_item_1.user_int_4 = 0
    _similar_item_1.user_int_5 = 0

    _similar_item_2 = RAMSTKSimilarItemRecord()
    _similar_item_2.revision_id = 1
    _similar_item_2.hardware_id = 2
    _similar_item_2.change_description_1 = ""
    _similar_item_2.change_description_2 = ""
    _similar_item_2.change_description_3 = ""
    _similar_item_2.change_description_4 = ""
    _similar_item_2.change_description_5 = ""
    _similar_item_2.change_description_6 = ""
    _similar_item_2.change_description_7 = ""
    _similar_item_2.change_description_8 = ""
    _similar_item_2.change_description_9 = ""
    _similar_item_2.change_description_10 = ""
    _similar_item_2.change_factor_1 = 1.0
    _similar_item_2.change_factor_2 = 1.0
    _similar_item_2.change_factor_3 = 1.0
    _similar_item_2.change_factor_4 = 1.0
    _similar_item_2.change_factor_5 = 1.0
    _similar_item_2.change_factor_6 = 1.0
    _similar_item_2.change_factor_7 = 1.0
    _similar_item_2.change_factor_8 = 1.0
    _similar_item_2.change_factor_9 = 1.0
    _similar_item_2.change_factor_10 = 1.0
    _similar_item_2.environment_from_id = 0
    _similar_item_2.environment_to_id = 0
    _similar_item_2.function_1 = "0"
    _similar_item_2.function_2 = "0"
    _similar_item_2.function_3 = "0"
    _similar_item_2.function_4 = "0"
    _similar_item_2.function_5 = "0"
    _similar_item_2.parent_id = 1
    _similar_item_2.similar_item_method_id = 1
    _similar_item_2.quality_from_id = 0
    _similar_item_2.quality_to_id = 0
    _similar_item_2.result_1 = 0.0
    _similar_item_2.result_2 = 0.0
    _similar_item_2.result_3 = 0.0
    _similar_item_2.result_4 = 0.0
    _similar_item_2.result_5 = 0.0
    _similar_item_2.temperature_from = 30.0
    _similar_item_2.temperature_to = 30.0
    _similar_item_2.user_blob_1 = ""
    _similar_item_2.user_blob_2 = ""
    _similar_item_2.user_blob_3 = ""
    _similar_item_2.user_blob_4 = ""
    _similar_item_2.user_blob_5 = ""
    _similar_item_2.user_float_1 = 0.0
    _similar_item_2.user_float_2 = 0.0
    _similar_item_2.user_float_3 = 0.0
    _similar_item_2.user_float_4 = 0.0
    _similar_item_2.user_float_5 = 0.0
    _similar_item_2.user_int_1 = 0
    _similar_item_2.user_int_2 = 0
    _similar_item_2.user_int_3 = 0
    _similar_item_2.user_int_4 = 0
    _similar_item_2.user_int_5 = 0

    _similar_item_3 = RAMSTKSimilarItemRecord()
    _similar_item_3.revision_id = 1
    _similar_item_3.hardware_id = 3
    _similar_item_3.change_description_1 = ""
    _similar_item_3.change_description_2 = ""
    _similar_item_3.change_description_3 = ""
    _similar_item_3.change_description_4 = ""
    _similar_item_3.change_description_5 = ""
    _similar_item_3.change_description_6 = ""
    _similar_item_3.change_description_7 = ""
    _similar_item_3.change_description_8 = ""
    _similar_item_3.change_description_9 = ""
    _similar_item_3.change_description_10 = ""
    _similar_item_3.change_factor_1 = 1.0
    _similar_item_3.change_factor_2 = 1.0
    _similar_item_3.change_factor_3 = 1.0
    _similar_item_3.change_factor_4 = 1.0
    _similar_item_3.change_factor_5 = 1.0
    _similar_item_3.change_factor_6 = 1.0
    _similar_item_3.change_factor_7 = 1.0
    _similar_item_3.change_factor_8 = 1.0
    _similar_item_3.change_factor_9 = 1.0
    _similar_item_3.change_factor_10 = 1.0
    _similar_item_3.environment_from_id = 0
    _similar_item_3.environment_to_id = 0
    _similar_item_3.function_1 = "0"
    _similar_item_3.function_2 = "0"
    _similar_item_3.function_3 = "0"
    _similar_item_3.function_4 = "0"
    _similar_item_3.function_5 = "0"
    _similar_item_3.parent_id = 1
    _similar_item_3.similar_item_method_id = 1
    _similar_item_3.quality_from_id = 0
    _similar_item_3.quality_to_id = 0
    _similar_item_3.result_1 = 0.0
    _similar_item_3.result_2 = 0.0
    _similar_item_3.result_3 = 0.0
    _similar_item_3.result_4 = 0.0
    _similar_item_3.result_5 = 0.0
    _similar_item_3.temperature_from = 30.0
    _similar_item_3.temperature_to = 30.0
    _similar_item_3.user_blob_1 = ""
    _similar_item_3.user_blob_2 = ""
    _similar_item_3.user_blob_3 = ""
    _similar_item_3.user_blob_4 = ""
    _similar_item_3.user_blob_5 = ""
    _similar_item_3.user_float_1 = 0.0
    _similar_item_3.user_float_2 = 0.0
    _similar_item_3.user_float_3 = 0.0
    _similar_item_3.user_float_4 = 0.0
    _similar_item_3.user_float_5 = 0.0
    _similar_item_3.user_int_1 = 0
    _similar_item_3.user_int_2 = 0
    _similar_item_3.user_int_3 = 0
    _similar_item_3.user_int_4 = 0
    _similar_item_3.user_int_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _similar_item_1,
        _similar_item_2,
        _similar_item_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 4,
        "change_description_1": "",
        "change_description_2": "",
        "change_description_3": "",
        "change_description_4": "",
        "change_description_5": "",
        "change_description_6": "",
        "change_description_7": "",
        "change_description_8": "",
        "change_description_9": "",
        "change_description_10": "",
        "change_factor_1": 1.0,
        "change_factor_2": 1.0,
        "change_factor_3": 1.0,
        "change_factor_4": 1.0,
        "change_factor_5": 1.0,
        "change_factor_6": 1.0,
        "change_factor_7": 1.0,
        "change_factor_8": 1.0,
        "change_factor_9": 1.0,
        "change_factor_10": 1.0,
        "environment_from_id": 0,
        "environment_to_id": 0,
        "function_1": "0",
        "function_2": "0",
        "function_3": "0",
        "function_4": "0",
        "function_5": "0",
        "parent_id": 1,
        "similar_item_method_id": 1,
        "quality_from_id": 0,
        "quality_to_id": 0,
        "result_1": 0.0,
        "result_2": 0.0,
        "result_3": 0.0,
        "result_4": 0.0,
        "result_5": 0.0,
        "temperature_from": 30.0,
        "temperature_to": 30.0,
        "user_blob_1": "",
        "user_blob_2": "",
        "user_blob_3": "",
        "user_blob_4": "",
        "user_blob_5": "",
        "user_float_1": 0.0,
        "user_float_2": 0.0,
        "user_float_3": 0.0,
        "user_float_4": 0.0,
        "user_float_5": 0.0,
        "user_int_1": 0,
        "user_int_2": 0,
        "user_int_3": 0,
        "user_int_4": 0,
        "user_int_5": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKSimilarItemRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
