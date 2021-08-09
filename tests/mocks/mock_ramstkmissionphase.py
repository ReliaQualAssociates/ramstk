# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKMissionPhase(MockRAMSTKBaseRecord):
    __defaults__ = {"description": "", "name": "", "phase_start": 0.0, "phase_end": 0.0}

    def __init__(self):
        self.revision_id = 0
        self.mission_id = 0
        self.phase_id = 0
        self.description = self.__defaults__["description"]
        self.name = self.__defaults__["name"]
        self.phase_start = self.__defaults__["phase_start"]
        self.phase_end = self.__defaults__["phase_end"]

        self.is_mission = False
        self.is_phase = True
        self.is_env = False

    def get_attributes(self):
        _attributes = {
            "mission_id": self.mission_id,
            "phase_id": self.phase_id,
            "description": self.description,
            "name": self.name,
            "phase_start": self.phase_start,
            "phase_end": self.phase_end,
        }

        return _attributes
