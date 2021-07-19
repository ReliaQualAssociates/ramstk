# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Package Imports
from ramstk.analyses.statistics import do_calculate_beta_bounds

# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKValidation(MockRAMSTKBaseTable):
    __defaults__ = {
        "acceptable_maximum": 0.0,
        "acceptable_mean": 0.0,
        "acceptable_minimum": 0.0,
        "acceptable_variance": 0.0,
        "confidence": 95.0,
        "cost_average": 0.0,
        "cost_ll": 0.0,
        "cost_maximum": 0.0,
        "cost_mean": 0.0,
        "cost_minimum": 0.0,
        "cost_ul": 0.0,
        "cost_variance": 0.0,
        "date_end": date.today() + timedelta(days=30),
        "date_start": date.today(),
        "description": "",
        "measurement_unit": "",
        "name": "",
        "status": 0.0,
        "task_type": "",
        "task_specification": "",
        "time_average": 0.0,
        "time_ll": 0.0,
        "time_maximum": 0.0,
        "time_mean": 0.0,
        "time_minimum": 0.0,
        "time_ul": 0.0,
        "time_variance": 0.0,
    }

    def __init__(self):
        self.revision_id = 0
        self.validation_id = 0
        self.acceptable_maximum = self.__defaults__["acceptable_maximum"]
        self.acceptable_mean = self.__defaults__["acceptable_mean"]
        self.acceptable_minimum = self.__defaults__["acceptable_minimum"]
        self.acceptable_variance = self.__defaults__["acceptable_variance"]
        self.confidence = self.__defaults__["confidence"]
        self.cost_average = self.__defaults__["cost_average"]
        self.cost_ll = self.__defaults__["cost_ll"]
        self.cost_maximum = self.__defaults__["cost_maximum"]
        self.cost_mean = self.__defaults__["cost_mean"]
        self.cost_minimum = self.__defaults__["cost_minimum"]
        self.cost_ul = self.__defaults__["cost_ul"]
        self.cost_variance = self.__defaults__["cost_variance"]
        self.date_end = self.__defaults__["date_end"]
        self.date_start = self.__defaults__["date_start"]
        self.description = self.__defaults__["description"]
        self.measurement_unit = self.__defaults__["measurement_unit"]
        self.name = self.__defaults__["name"]
        self.status = self.__defaults__["status"]
        self.task_specification = self.__defaults__["task_specification"]
        self.task_type = self.__defaults__["task_type"]
        self.time_average = self.__defaults__["time_average"]
        self.time_ll = self.__defaults__["time_ll"]
        self.time_maximum = self.__defaults__["time_maximum"]
        self.time_mean = self.__defaults__["time_mean"]
        self.time_minimum = self.__defaults__["time_minimum"]
        self.time_ul = self.__defaults__["time_ul"]
        self.time_variance = self.__defaults__["time_variance"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "validation_id": self.validation_id,
            "acceptable_maximum": self.acceptable_maximum,
            "acceptable_mean": self.acceptable_mean,
            "acceptable_minimum": self.acceptable_minimum,
            "acceptable_variance": self.acceptable_variance,
            "confidence": self.confidence,
            "cost_average": self.cost_average,
            "cost_ll": self.cost_ll,
            "cost_maximum": self.cost_maximum,
            "cost_mean": self.cost_mean,
            "cost_minimum": self.cost_minimum,
            "cost_ul": self.cost_ul,
            "cost_variance": self.cost_variance,
            "date_end": self.date_end,
            "date_start": self.date_start,
            "description": self.description,
            "measurement_unit": self.measurement_unit,
            "name": self.name,
            "status": self.status,
            "task_specification": self.task_specification,
            "task_type": self.task_type,
            "time_average": self.time_average,
            "time_ll": self.time_ll,
            "time_maximum": self.time_maximum,
            "time_mean": self.time_mean,
            "time_minimum": self.time_minimum,
            "time_ul": self.time_ul,
            "time_variance": self.time_variance,
        }

        return _attributes

    def calculate_task_time(self):
        (self.time_ll, self.time_mean, self.time_ul, _sd) = do_calculate_beta_bounds(
            self.time_minimum, self.time_average, self.time_maximum, self.confidence
        )

        self.time_variance = _sd ** 2.0

    def calculate_task_cost(self):
        (self.cost_ll, self.cost_mean, self.cost_ul, _sd) = do_calculate_beta_bounds(
            self.cost_minimum, self.cost_average, self.cost_maximum, self.confidence
        )

        self.cost_variance = _sd ** 2.0
