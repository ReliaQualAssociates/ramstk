# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKMission(MockRAMSTKBaseTable):
    __defaults__ = {"description": "", "mission_time": 0.0, "time_units": "hours"}

    def __init__(self):
        self.revision_id = 0
        self.mission_id = 0
        self.description = self.__defaults__["description"]
        self.mission_time = self.__defaults__["mission_time"]
        self.time_units = self.__defaults__["time_units"]

        self.is_mission = True
        self.is_phase = False
        self.is_env = False

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "mission_id": self.mission_id,
            "description": self.description,
            "mission_time": self.mission_time,
            "time_units": self.time_units,
        }

        return _attributes
