# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.fmea.record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Date, Float, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord


class RAMSTKFMEARecord(RAMSTK_BASE, RAMSTKBaseRecord):
    """Class to represent view fmeca in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_function. This table
    shares a Many-to-One relationship with ramstk_hardware. This table shares a
    One-to-Many relationship with ramstk_mechanism.
    """

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
    __tablename__ = "ramstk_fmeca"
    __table_args__ = ({"extend_existing": True},)

    revision_id = Column("fld_revision_id", Integer, primary_key=True, nullable=False)
    hardware_id = Column("fld_hardware_id", Integer, primary_key=True, nullable=False)
    mode_id = Column("fld_mode_id", Integer, primary_key=True, nullable=False)
    mechanism_id = Column("fld_mechanism_id", Integer, primary_key=True, nullable=False)
    cause_id = Column("fld_cause_id", Integer, primary_key=True, nullable=False)
    control_id = Column("fld_control_id", Integer, primary_key=True, nullable=False)
    action_id = Column("fld_action_id", Integer, primary_key=True, nullable=False)
    mode_description = Column("md_description", String)
    mechanism_description = Column("mc_description", String)
    cause_description = Column("cs_description", String)
    control_description = Column("ct_description", String)
    action_description = Column("ac_description", String)
    mission = Column("fld_mission", String(64))
    mission_phase = Column("fld_mission_phase", String(64))
    effect_local = Column("fld_effect_local", String(512))
    effect_next = Column("fld_effect_next", String(512))
    effect_end = Column("fld_effect_end", String(512))
    detection_method = Column("fld_detection_method", String(512))
    other_indications = Column("fld_other_indications", String(512))
    isolation_method = Column("fld_isolation_method", String(512))
    design_provisions = Column("fld_design_provisions", String)
    operator_actions = Column("fld_operator_actions", String)
    severity_class = Column("fld_severity_class", String(64))
    hazard_rate_source = Column("fld_hazard_rate_source", String(512))
    mode_probability = Column("fld_mode_probability", String(64))
    effect_probability = Column("fld_effect_probability", Float)
    hazard_rate_active = Column("fld_hazard_rate_active", Float)
    mode_ratio = Column("fld_mode_ratio", Float)
    mode_hazard_rate = Column("fld_mode_hazard_rate", Float)
    mode_op_time = Column("fld_mode_op_time", Float)
    mode_criticality = Column("fld_mode_criticality", Float)
    type_id = Column("fld_type_id", Integer)
    rpn_severity = Column("fld_rpn_severity", Integer)
    rpn_occurrence = Column("fld_rpn_occurrence", Integer)
    rpn_detection = Column("fld_rpn_detection", Integer)
    rpn = Column("fld_rpn", Integer)
    action_category = Column("fld_action_category", String(512))
    action_owner = Column("fld_action_owner", String(512))
    action_due_date = Column("fld_action_due_date", Date)
    action_status = Column("fld_action_status", String(512))
    action_taken = Column("fld_action_taken", String)
    action_approved = Column("fld_action_approved", Integer)
    action_approve_date = Column("fld_action_approve_date", Date)
    action_closed = Column("fld_action_closed", Integer)
    action_close_date = Column("fld_action_close_date", Date)
    rpn_severity_new = Column("fld_rpn_severity_new", Integer)
    rpn_occurrence_new = Column("fld_rpn_occurrence_new", Integer)
    rpn_detection_new = Column("fld_rpn_detection_new", Integer)
    rpn_new = Column("fld_rpn_new", Integer)
    single_point = Column("fld_single_point", Integer)
    pof_include = Column("fld_pof_include", Integer)
    remarks = Column("fld_remarks", String)
    hardware_description = Column("hw_description", String)

    def get_attributes(self) -> Dict[str, Union[float, int, str]]:
        """Retrieve the current values of the RAMSTKFMEA data model attributes.

        :return: {revision_id, hardware_id, mode_id, mechanism_id,
                  cause_id, control_id, action_id, critical_item,
                  description, design_provisions, detection_method,
                  effect_end, effect_local, effect_next, effect_probability,
                  hazard_rate_source, isolation_method, mission, mission_phase,
                  mode_criticality, mode_hazard_rate, mode_op_time,
                  mode_probability, mode_ratio, operator_actions,
                  other_indications, remarks, rpn_severity, rpn_severity_new,
                  severity_class, single_point, type_id} pairs.
        :rtype: dict
        """
        _attributes = {
            "fld_revision_id": self.revision_id,
            "fld_hardware_id": self.hardware_id,
            "fld_mode_id": self.mode_id,
            "fld_mechanism_id": self.mechanism_id,
            "fld_cause_id": self.cause_id,
            "fld_control_id": self.control_id,
            "fld_action_id": self.action_id,
            "mc_description": self.mechanism_description,
            "cs_description": self.cause_description,
            "ct_description": self.control_description,
            "ac_description": self.action_description,
            "fld_mission": self.mission,
            "fld_mission_phase": self.mission_phase,
            "fld_effect_local": self.effect_local,
            "fld_effect_next": self.effect_next,
            "fld_effect_end": self.effect_end,
            "fld_detection_method": self.detection_method,
            "fld_other_indications": self.other_indications,
            "fld_isolation_method": self.isolation_method,
            "fld_design_provisions": self.design_provisions,
            "fld_operator_actions": self.operator_actions,
            "fld_severity_class": self.severity_class,
            "fld_hazard_rate_source": self.hazard_rate_source,
            "fld_mode_probability": self.mode_probability,
            "fld_effect_probability": self.effect_probability,
            "fld_hazard_rate_active": self.hazard_rate_active,
            "fld_mode_ratio": self.mode_ratio,
            "fld_mode_hazard_rate": self.mode_hazard_rate,
            "fld_mode_op_time": self.mode_op_time,
            "fld_mode_criticality": self.mode_criticality,
            "fld_type_id": self.type_id,
            "fld_rpn_severity": self.rpn_severity,
            "fld_rpn_occurrence": self.rpn_occurrence,
            "fld_rpn_detection": self.rpn_detection,
            "fld_rpn": self.rpn,
            "fld_action_category": self.action_category,
            "fld_action_owner": self.action_owner,
            "fld_action_due_date": self.action_due_date,
            "fld_action_status": self.action_status,
            "fld_action_taken": self.action_taken,
            "fld_action_approved": self.action_approved,
            "fld_action_approve_date": self.action_approve_date,
            "fld_action_closed": self.action_closed,
            "fld_action_close_date": self.action_close_date,
            "fld_rpn_severity_new": self.rpn_severity_new,
            "fld_rpn_occurrence_new": self.rpn_occurrence_new,
            "fld_rpn_detection_new": self.rpn_detection_new,
            "fld_rpn_new": self.rpn_new,
            "fld_single_point": self.single_point,
            "fld_pof_include": self.pof_include,
            "fld_remarks": self.remarks,
            "hw_description": self.hardware_description,
        }

        return _attributes
