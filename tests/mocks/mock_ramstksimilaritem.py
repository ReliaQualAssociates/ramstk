# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKSimilarItem(MockRAMSTKBaseTable):
    __defaults__ = {
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
        "similar_item_method_id": 1,
        "parent_id": 0,
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

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.change_description_1 = self.__defaults__["change_description_1"]
        self.change_description_2 = self.__defaults__["change_description_2"]
        self.change_description_3 = self.__defaults__["change_description_3"]
        self.change_description_4 = self.__defaults__["change_description_4"]
        self.change_description_5 = self.__defaults__["change_description_5"]
        self.change_description_6 = self.__defaults__["change_description_6"]
        self.change_description_7 = self.__defaults__["change_description_7"]
        self.change_description_8 = self.__defaults__["change_description_8"]
        self.change_description_9 = self.__defaults__["change_description_9"]
        self.change_description_10 = self.__defaults__["change_description_10"]
        self.change_factor_1 = self.__defaults__["change_factor_1"]
        self.change_factor_2 = self.__defaults__["change_factor_2"]
        self.change_factor_3 = self.__defaults__["change_factor_3"]
        self.change_factor_4 = self.__defaults__["change_factor_4"]
        self.change_factor_5 = self.__defaults__["change_factor_5"]
        self.change_factor_6 = self.__defaults__["change_factor_6"]
        self.change_factor_7 = self.__defaults__["change_factor_7"]
        self.change_factor_8 = self.__defaults__["change_factor_8"]
        self.change_factor_9 = self.__defaults__["change_factor_9"]
        self.change_factor_10 = self.__defaults__["change_factor_10"]
        self.environment_from_id = self.__defaults__["environment_from_id"]
        self.environment_to_id = self.__defaults__["environment_to_id"]
        self.function_1 = self.__defaults__["function_1"]
        self.function_2 = self.__defaults__["function_2"]
        self.function_3 = self.__defaults__["function_3"]
        self.function_4 = self.__defaults__["function_4"]
        self.function_5 = self.__defaults__["function_5"]
        self.similar_item_method_id = self.__defaults__["similar_item_method_id"]
        self.parent_id = self.__defaults__["parent_id"]
        self.quality_from_id = self.__defaults__["quality_from_id"]
        self.quality_to_id = self.__defaults__["quality_to_id"]
        self.result_1 = self.__defaults__["result_1"]
        self.result_2 = self.__defaults__["result_2"]
        self.result_3 = self.__defaults__["result_3"]
        self.result_4 = self.__defaults__["result_4"]
        self.result_5 = self.__defaults__["result_5"]
        self.temperature_from = self.__defaults__["temperature_from"]
        self.temperature_to = self.__defaults__["temperature_to"]
        self.user_blob_1 = self.__defaults__["user_blob_1"]
        self.user_blob_2 = self.__defaults__["user_blob_2"]
        self.user_blob_3 = self.__defaults__["user_blob_3"]
        self.user_blob_4 = self.__defaults__["user_blob_4"]
        self.user_blob_5 = self.__defaults__["user_blob_5"]
        self.user_float_1 = self.__defaults__["user_float_1"]
        self.user_float_2 = self.__defaults__["user_float_2"]
        self.user_float_3 = self.__defaults__["user_float_3"]
        self.user_float_4 = self.__defaults__["user_float_4"]
        self.user_float_5 = self.__defaults__["user_float_5"]
        self.user_int_1 = self.__defaults__["user_int_1"]
        self.user_int_2 = self.__defaults__["user_int_2"]
        self.user_int_3 = self.__defaults__["user_int_3"]
        self.user_int_4 = self.__defaults__["user_int_4"]
        self.user_int_5 = self.__defaults__["user_int_5"]

    def get_attributes(self):
        _attributes = {
            "hardware_id": self.hardware_id,
            "change_description_1": self.change_description_1,
            "change_description_2": self.change_description_2,
            "change_description_3": self.change_description_3,
            "change_description_4": self.change_description_4,
            "change_description_5": self.change_description_5,
            "change_description_6": self.change_description_6,
            "change_description_7": self.change_description_7,
            "change_description_8": self.change_description_8,
            "change_description_9": self.change_description_9,
            "change_description_10": self.change_description_10,
            "change_factor_1": self.change_factor_1,
            "change_factor_2": self.change_factor_2,
            "change_factor_3": self.change_factor_3,
            "change_factor_4": self.change_factor_4,
            "change_factor_5": self.change_factor_5,
            "change_factor_6": self.change_factor_6,
            "change_factor_7": self.change_factor_7,
            "change_factor_8": self.change_factor_8,
            "change_factor_9": self.change_factor_9,
            "change_factor_10": self.change_factor_10,
            "environment_from_id": self.environment_from_id,
            "environment_to_id": self.environment_to_id,
            "function_1": self.function_1,
            "function_2": self.function_2,
            "function_3": self.function_3,
            "function_4": self.function_4,
            "function_5": self.function_5,
            "similar_item_method_id": self.similar_item_method_id,
            "parent_id": self.parent_id,
            "quality_from_id": self.quality_from_id,
            "quality_to_id": self.quality_to_id,
            "result_1": self.result_1,
            "result_2": self.result_2,
            "result_3": self.result_3,
            "result_4": self.result_4,
            "result_5": self.result_5,
            "temperature_from": self.temperature_from,
            "temperature_to": self.temperature_to,
            "user_blob_1": self.user_blob_1,
            "user_blob_2": self.user_blob_2,
            "user_blob_3": self.user_blob_3,
            "user_blob_4": self.user_blob_4,
            "user_blob_5": self.user_blob_5,
            "user_float_1": self.user_float_1,
            "user_float_2": self.user_float_2,
            "user_float_3": self.user_float_3,
            "user_float_4": self.user_float_4,
            "user_float_5": self.user_float_5,
            "user_int_1": self.user_int_1,
            "user_int_2": self.user_int_2,
            "user_int_3": self.user_int_3,
            "user_int_4": self.user_int_4,
            "user_int_5": self.user_int_5,
        }

        return _attributes
