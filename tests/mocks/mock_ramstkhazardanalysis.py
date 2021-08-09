# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKHazardAnalysis(MockRAMSTKBaseRecord):
    __defaults__ = {
        "potential_hazard": "",
        "potential_cause": "",
        "assembly_effect": "",
        "assembly_severity": "Major",
        "assembly_probability": "Level A - Frequent",
        "assembly_hri": 20,
        "assembly_mitigation": "",
        "assembly_severity_f": "Major",
        "assembly_probability_f": "Level A - Frequent",
        "assembly_hri_f": 20,
        "function_1": "",
        "function_2": "",
        "function_3": "",
        "function_4": "",
        "function_5": "",
        "remarks": "",
        "result_1": 0.0,
        "result_2": 0.0,
        "result_3": 0.0,
        "result_4": 0.0,
        "result_5": 0.0,
        "system_effect": "",
        "system_severity": "Major",
        "system_probability": "Level A - Frequent",
        "system_hri": 20,
        "system_mitigation": "",
        "system_severity_f": "Major",
        "system_probability_f": "Level A - Frequent",
        "system_hri_f": 20,
        "user_blob_1": "",
        "user_blob_2": "",
        "user_blob_3": "",
        "user_float_1": 0.0,
        "user_float_2": 0.0,
        "user_float_3": 0.0,
        "user_int_1": 0,
        "user_int_2": 0,
        "user_int_3": 0,
    }

    def __init__(self):
        self.revision_id = 0
        self.function_id = 0
        self.hazard_id = 0
        self.potential_hazard = self.__defaults__["potential_hazard"]
        self.potential_cause = self.__defaults__["potential_cause"]
        self.assembly_effect = self.__defaults__["assembly_effect"]
        self.assembly_severity = self.__defaults__["assembly_severity"]
        self.assembly_probability = self.__defaults__["assembly_probability"]
        self.assembly_hri = self.__defaults__["assembly_hri"]
        self.assembly_mitigation = self.__defaults__["assembly_mitigation"]
        self.assembly_severity_f = self.__defaults__["assembly_severity_f"]
        self.assembly_probability_f = self.__defaults__["assembly_probability_f"]
        self.assembly_hri_f = self.__defaults__["assembly_hri_f"]
        self.function_1 = self.__defaults__["function_1"]
        self.function_2 = self.__defaults__["function_2"]
        self.function_3 = self.__defaults__["function_3"]
        self.function_4 = self.__defaults__["function_4"]
        self.function_5 = self.__defaults__["function_5"]
        self.remarks = self.__defaults__["remarks"]
        self.result_1 = self.__defaults__["result_1"]
        self.result_2 = self.__defaults__["result_2"]
        self.result_3 = self.__defaults__["result_3"]
        self.result_4 = self.__defaults__["result_4"]
        self.result_5 = self.__defaults__["result_5"]
        self.system_effect = self.__defaults__["system_effect"]
        self.system_severity = self.__defaults__["system_severity"]
        self.system_probability = self.__defaults__["system_probability"]
        self.system_hri = self.__defaults__["system_hri"]
        self.system_mitigation = self.__defaults__["system_mitigation"]
        self.system_severity_f = self.__defaults__["system_severity_f"]
        self.system_probability_f = self.__defaults__["system_probability_f"]
        self.system_hri_f = self.__defaults__["system_hri_f"]
        self.user_blob_1 = self.__defaults__["user_blob_1"]
        self.user_blob_2 = self.__defaults__["user_blob_2"]
        self.user_blob_3 = self.__defaults__["user_blob_3"]
        self.user_float_1 = self.__defaults__["user_float_1"]
        self.user_float_2 = self.__defaults__["user_float_2"]
        self.user_float_3 = self.__defaults__["user_float_3"]
        self.user_int_1 = self.__defaults__["user_int_1"]
        self.user_int_2 = self.__defaults__["user_int_2"]
        self.user_int_3 = self.__defaults__["user_int_3"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "function_id": self.function_id,
            "hazard_id": self.hazard_id,
            "potential_hazard": self.potential_hazard,
            "potential_cause": self.potential_cause,
            "assembly_effect": self.assembly_effect,
            "assembly_severity": self.assembly_severity,
            "assembly_probability": self.assembly_probability,
            "assembly_hri": self.assembly_hri,
            "assembly_mitigation": self.assembly_mitigation,
            "assembly_severity_f": self.assembly_severity_f,
            "assembly_probability_f": self.assembly_probability_f,
            "assembly_hri_f": self.assembly_hri_f,
            "system_effect": self.system_effect,
            "system_severity": self.system_severity,
            "system_probability": self.system_probability,
            "system_hri": self.system_hri,
            "system_mitigation": self.system_mitigation,
            "system_severity_f": self.system_severity_f,
            "system_probability_f": self.system_probability_f,
            "system_hri_f": self.system_hri_f,
            "remarks": self.remarks,
            "function_1": self.function_1,
            "function_2": self.function_2,
            "function_3": self.function_3,
            "function_4": self.function_4,
            "function_5": self.function_5,
            "result_1": self.result_1,
            "result_2": self.result_2,
            "result_3": self.result_3,
            "result_4": self.result_4,
            "result_5": self.result_5,
            "user_blob_1": self.user_blob_1,
            "user_blob_2": self.user_blob_2,
            "user_blob_3": self.user_blob_3,
            "user_float_1": self.user_float_1,
            "user_float_2": self.user_float_2,
            "user_float_3": self.user_float_3,
            "user_int_1": self.user_int_1,
            "user_int_2": self.user_int_2,
            "user_int_3": self.user_int_3,
        }

        return _attributes
