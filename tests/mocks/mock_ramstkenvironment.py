# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKEnvironment(MockRAMSTKBaseRecord):
    __defaults__ = {
        "name": "Condition Name",
        "units": "Units",
        "minimum": 0.0,
        "maximum": 0.0,
        "mean": 0.0,
        "variance": 0.0,
        "ramp_rate": 0.0,
        "low_dwell_time": 0.0,
        "high_dwell_time": 0.0,
    }
    __tablename__ = "ramstk_environment"
    __table_args__ = {"extend_existing": True}

    def __init__(self):
        self.revision_id = 0
        self.phase_id = 0
        self.environment_id = 0

        self.name = self.__defaults__["name"]
        self.units = self.__defaults__["units"]
        self.minimum = self.__defaults__["minimum"]
        self.maximum = self.__defaults__["maximum"]
        self.mean = self.__defaults__["mean"]
        self.variance = self.__defaults__["variance"]
        self.ramp_rate = self.__defaults__["ramp_rate"]
        self.low_dwell_time = self.__defaults__["low_dwell_time"]
        self.high_dwell_time = self.__defaults__["high_dwell_time"]

        self.is_mission = False
        self.is_phase = False
        self.is_env = True

    def get_attributes(self):
        _attributes = {
            "phase_id": self.phase_id,
            "environment_id": self.environment_id,
            "name": self.name,
            "units": self.units,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "mean": self.mean,
            "variance": self.variance,
            "ramp_rate": self.ramp_rate,
            "low_dwell_time": self.low_dwell_time,
            "high_dwell_time": self.high_dwell_time,
        }

        return _attributes
