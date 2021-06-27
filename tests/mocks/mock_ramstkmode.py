# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKMode(MockRAMSTKBaseTable):
    __defaults__ = {
        "critical_item": 0,
        "description": "",
        "design_provisions": "",
        "detection_method": "",
        "effect_end": "",
        "effect_local": "",
        "effect_next": "",
        "effect_probability": 0.0,
        "hazard_rate_source": "",
        "isolation_method": "",
        "mission": "Default Mission",
        "mission_phase": "",
        "mode_criticality": 0.0,
        "mode_hazard_rate": 0.0,
        "mode_op_time": 0.0,
        "mode_probability": "",
        "mode_ratio": 0.0,
        "operator_actions": "",
        "other_indications": "",
        "remarks": "",
        "rpn_severity": 1,
        "rpn_severity_new": 1,
        "severity_class": "",
        "single_point": 0,
        "type_id": 0,
    }

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.critical_item = self.__defaults__["critical_item"]
        self.description = self.__defaults__["description"]
        self.design_provisions = self.__defaults__["design_provisions"]
        self.detection_method = self.__defaults__["detection_method"]
        self.effect_end = self.__defaults__["effect_end"]
        self.effect_local = self.__defaults__["effect_local"]
        self.effect_next = self.__defaults__["effect_next"]
        self.effect_probability = self.__defaults__["effect_probability"]
        self.hazard_rate_source = self.__defaults__["hazard_rate_source"]
        self.isolation_method = self.__defaults__["isolation_method"]
        self.mission = self.__defaults__["mission"]
        self.mission_phase = self.__defaults__["mission_phase"]
        self.mode_criticality = self.__defaults__["mode_criticality"]
        self.mode_hazard_rate = self.__defaults__["mode_hazard_rate"]
        self.mode_op_time = self.__defaults__["mode_op_time"]
        self.mode_probability = self.__defaults__["mode_probability"]
        self.mode_ratio = self.__defaults__["mode_ratio"]
        self.operator_actions = self.__defaults__["operator_actions"]
        self.other_indications = self.__defaults__["other_indications"]
        self.remarks = self.__defaults__["remarks"]
        self.rpn_severity = self.__defaults__["rpn_severity"]
        self.rpn_severity_new = self.__defaults__["rpn_severity_new"]
        self.severity_class = self.__defaults__["severity_class"]
        self.single_point = self.__defaults__["single_point"]
        self.type_id = self.__defaults__["type_id"]

        self.is_mode = True
        self.is_mechanism = False
        self.is_cause = False
        self.is_control = False
        self.is_action = False
        self.is_opload = False
        self.is_opstress = False
        self.is_testmethod = False

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "hardware_id": self.hardware_id,
            "mode_id": self.mode_id,
            "critical_item": self.critical_item,
            "description": self.description,
            "design_provisions": self.design_provisions,
            "detection_method": self.detection_method,
            "effect_end": self.effect_end,
            "effect_local": self.effect_local,
            "effect_next": self.effect_next,
            "effect_probability": self.effect_probability,
            "hazard_rate_source": self.hazard_rate_source,
            "isolation_method": self.isolation_method,
            "mission": self.mission,
            "mission_phase": self.mission_phase,
            "mode_criticality": self.mode_criticality,
            "mode_hazard_rate": self.mode_hazard_rate,
            "mode_op_time": self.mode_op_time,
            "mode_probability": self.mode_probability,
            "mode_ratio": self.mode_ratio,
            "operator_actions": self.operator_actions,
            "other_indications": self.other_indications,
            "remarks": self.remarks,
            "rpn_severity": self.rpn_severity,
            "rpn_severity_new": self.rpn_severity_new,
            "severity_class": self.severity_class,
            "single_point": self.single_point,
            "type_id": self.type_id,
        }

        return _attributes
