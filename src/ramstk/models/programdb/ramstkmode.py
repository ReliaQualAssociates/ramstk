# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.ramstkmode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMode Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMode(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_mode in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_function.
    This table shares a Many-to-One relationship with ramstk_hardware.
    This table shares a One-to-Many relationship with ramstk_mechanism.
    """

    __defaults__ = {
        'critical_item': 0,
        'description': '',
        'design_provisions': '',
        'detection_method': '',
        'effect_end': '',
        'effect_local': '',
        'effect_next': '',
        'effect_probability': 0.0,
        'hazard_rate_source': '',
        'isolation_method': '',
        'mission': 'Default Mission',
        'mission_phase': '',
        'mode_criticality': 0.0,
        'mode_hazard_rate': 0.0,
        'mode_op_time': 0.0,
        'mode_probability': '',
        'mode_ratio': 0.0,
        'operator_actions': '',
        'other_indications': '',
        'remarks': '',
        'rpn_severity': 1,
        'rpn_severity_new': 1,
        'severity_class': '',
        'single_point': 0,
        'type_id': 0
    }
    __tablename__ = 'ramstk_mode'
    __table_args__ = (ForeignKeyConstraint(
        ['fld_revision_id', 'fld_hardware_id'],
        ['ramstk_hardware.fld_revision_id', 'ramstk_hardware.fld_hardware_id'],
    ), {
        'extend_existing': True
    })

    revision_id = Column('fld_revision_id',
                         Integer,
                         primary_key=True,
                         nullable=False)
    hardware_id = Column('fld_hardware_id',
                         Integer,
                         primary_key=True,
                         default=-1,
                         nullable=False)
    mode_id = Column('fld_mode_id',
                     Integer,
                     primary_key=True,
                     autoincrement=True,
                     nullable=False)

    critical_item = Column('fld_critical_item',
                           Integer,
                           default=__defaults__['critical_item'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    design_provisions = Column('fld_design_provisions',
                               String,
                               default=__defaults__['design_provisions'])
    detection_method = Column('fld_detection_method',
                              String(512),
                              default=__defaults__['detection_method'])
    effect_end = Column('fld_effect_end',
                        String(512),
                        default=__defaults__['effect_end'])
    effect_local = Column('fld_effect_local',
                          String(512),
                          default=__defaults__['effect_local'])
    effect_next = Column('fld_effect_next',
                         String(512),
                         default=__defaults__['effect_next'])
    effect_probability = Column('fld_effect_probability',
                                Float,
                                default=__defaults__['effect_probability'])
    hazard_rate_source = Column('fld_hazard_rate_source',
                                String(512),
                                default=__defaults__['hazard_rate_source'])
    isolation_method = Column('fld_isolation_method',
                              String(512),
                              default=__defaults__['isolation_method'])
    mission = Column('fld_mission',
                     String(64),
                     default=__defaults__['mission'])
    mission_phase = Column('fld_mission_phase',
                           String(64),
                           default=__defaults__['mission_phase'])
    mode_criticality = Column('fld_mode_criticality',
                              Float,
                              default=__defaults__['mode_criticality'])
    mode_hazard_rate = Column('fld_mode_hazard_rate',
                              Float,
                              default=__defaults__['mode_hazard_rate'])
    mode_op_time = Column('fld_mode_op_time',
                          Float,
                          default=__defaults__['mode_op_time'])
    mode_probability = Column('fld_mode_probability',
                              String(64),
                              default=__defaults__['mode_probability'])
    mode_ratio = Column('fld_mode_ratio',
                        Float,
                        default=__defaults__['mode_ratio'])
    operator_actions = Column('fld_operator_actions',
                              String,
                              default=__defaults__['operator_actions'])
    other_indications = Column('fld_other_indications',
                               String(512),
                               default=__defaults__['other_indications'])
    remarks = Column('fld_remarks', String, default=__defaults__['remarks'])
    rpn_severity = Column('fld_rpn_severity',
                          Integer,
                          default=__defaults__['rpn_severity'])
    rpn_severity_new = Column('fld_rpn_severity_new',
                              Integer,
                              default=__defaults__['rpn_severity_new'])
    severity_class = Column('fld_severity_class',
                            String(64),
                            default=__defaults__['severity_class'])
    single_point = Column('fld_single_point',
                          Integer,
                          default=__defaults__['single_point'])
    type_id = Column('fld_type_id', Integer, default=__defaults__['type_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    mechanism = relationship(  # type: ignore
        'RAMSTKMechanism',
        back_populates='mode',
        cascade='all,delete',
    )

    is_mode = True
    is_mechanism = False
    is_cause = False
    is_control = False
    is_action = False
    is_opload = False
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """Retrieve the current values of the RAMSTKMode data model attributes.

        :return: {revision_id, hardware_id, mode_id, critical_item,
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
            'revision_id': self.revision_id,
            'hardware_id': self.hardware_id,
            'mode_id': self.mode_id,
            'critical_item': self.critical_item,
            'description': self.description,
            'design_provisions': self.design_provisions,
            'detection_method': self.detection_method,
            'effect_end': self.effect_end,
            'effect_local': self.effect_local,
            'effect_next': self.effect_next,
            'effect_probability': self.effect_probability,
            'hazard_rate_source': self.hazard_rate_source,
            'isolation_method': self.isolation_method,
            'mission': self.mission,
            'mission_phase': self.mission_phase,
            'mode_criticality': self.mode_criticality,
            'mode_hazard_rate': self.mode_hazard_rate,
            'mode_op_time': self.mode_op_time,
            'mode_probability': self.mode_probability,
            'mode_ratio': self.mode_ratio,
            'operator_actions': self.operator_actions,
            'other_indications': self.other_indications,
            'remarks': self.remarks,
            'rpn_severity': self.rpn_severity,
            'rpn_severity_new': self.rpn_severity_new,
            'severity_class': self.severity_class,
            'single_point': self.single_point,
            'type_id': self.type_id,
        }

        return _attributes
