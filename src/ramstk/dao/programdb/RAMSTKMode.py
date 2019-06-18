# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKMode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMode Table Module."""

# Standard Library Imports
import gettext

# Third Party Imports
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import OutOfRangeError, none_to_default

_ = gettext.gettext


class RAMSTKMode(RAMSTK_BASE):
    """
    Class to represent table ramstk_mode in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_function.
    This table shares a Many-to-One relationship with ramstk_hardware.
    This table shares a One-to-Many relationship with ramstk_mechanism.
    """

    __tablename__ = 'ramstk_mode'
    __table_args__ = {'extend_existing': True}

    function_id = Column(
        'fld_function_id',
        Integer,
        ForeignKey('ramstk_function.fld_function_id'),
        default=-1,
        nullable=False,
    )
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        default=-1,
        nullable=False,
    )
    mode_id = Column(
        'fld_mode_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    critical_item = Column('fld_critial_item', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    design_provisions = Column('fld_design_provisions', BLOB, default=b'')
    detection_method = Column('fld_detection_method', String(512), default='')
    effect_end = Column('fld_effect_end', String(512), default='')
    effect_local = Column('fld_effect_local', String(512), default='')
    effect_next = Column('fld_effect_next', String(512), default='')
    effect_probability = Column('fld_effect_probability', Float, default=0.0)
    hazard_rate_source = Column(
        'fld_hazard_rate_source', String(512), default='',
    )
    isolation_method = Column('fld_isolation_method', String(512), default='')
    mission = Column('fld_mission', String(64), default='Default Mission')
    mission_phase = Column('fld_mission_phase', String(64), default='')
    mode_criticality = Column('fld_mode_criticality', Float, default=0.0)
    mode_hazard_rate = Column('fld_mode_hazard_rate', Float, default=0.0)
    mode_op_time = Column('fld_mode_op_time', Float, default=0.0)
    mode_probability = Column('fld_mode_probability', String(64), default='')
    mode_ratio = Column('fld_mode_ratio', Float, default=0.0)
    operator_actions = Column('fld_operator_actions', BLOB, default=b'')
    other_indications = Column(
        'fld_other_indications', String(512), default='',
    )
    remarks = Column('fld_remarks', BLOB, default=b'')
    rpn_severity = Column('fld_rpn_severity', Integer, default=1)
    rpn_severity_new = Column('fld_rpn_severity_new', Integer, default=1)
    severity_class = Column('fld_severity_class', String(64), default='')
    single_point = Column('fld_single_point', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    function = relationship('RAMSTKFunction', back_populates='mode')
    hardware = relationship('RAMSTKHardware', back_populates='mode')
    mechanism = relationship(
        'RAMSTKMechanism', back_populates='mode', cascade='all,delete',
    )
    cause = relationship(
        'RAMSTKCause', back_populates='mode', cascade='all,delete',
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
        """
        Retrieve the current values of the RAMSTKMode data model attributes.

        :return: {function_id, hardware_id, mode_id, critical_item,
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
            'function_id': self.function_id,
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

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKMode data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMode {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.critical_item = int(
                none_to_default(attributes['critical_item'], 0),
            )
            self.description = str(
                none_to_default(
                    attributes['description'],
                    'Failure Mode Description',
                ),
            )
            self.design_provisions = none_to_default(
                attributes['design_provisions'], b'',
            )
            self.detection_method = str(
                none_to_default(attributes['detection_method'], ''),
            )
            self.effect_end = str(
                none_to_default(attributes['effect_end'], 'End Effect'),
            )
            self.effect_local = str(
                none_to_default(attributes['effect_local'], 'Local Effect'),
            )
            self.effect_next = str(
                none_to_default(attributes['effect_next'], 'Next Effect'),
            )
            self.effect_probability = float(
                none_to_default(attributes['effect_probability'], 0.0),
            )
            self.hazard_rate_source = str(
                none_to_default(attributes['hazard_rate_source'], ''),
            )
            self.isolation_method = str(
                none_to_default(attributes['isolation_method'], ''),
            )
            self.mission = str(none_to_default(attributes['mission'], ''))
            self.mission_phase = str(
                none_to_default(attributes['mission_phase'], ''),
            )
            self.mode_criticality = float(
                none_to_default(attributes['mode_criticality'], 0.0),
            )
            self.mode_hazard_rate = float(
                none_to_default(attributes['mode_hazard_rate'], 0.0),
            )
            self.mode_op_time = float(
                none_to_default(attributes['mode_op_time'], 0.0),
            )
            self.mode_probability = str(
                none_to_default(attributes['mode_probability'], ''),
            )
            self.mode_ratio = float(
                none_to_default(attributes['mode_ratio'], 0.0),
            )
            self.operator_actions = none_to_default(
                attributes['operator_actions'], b'',
            )
            self.other_indications = str(
                none_to_default(attributes['other_indications'], ''),
            )
            self.remarks = none_to_default(attributes['remarks'], b'')
            self.rpn_severity = int(
                none_to_default(attributes['rpn_severity'], 1),
            )
            self.rpn_severity_new = int(
                none_to_default(attributes['rpn_severity_new'], 1),
            )
            self.severity_class = str(
                none_to_default(attributes['severity_class'], ''),
            )
            self.single_point = int(
                none_to_default(attributes['single_point'], 0),
            )
            self.type_id = int(none_to_default(attributes['type_id'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKMode.set_attributes().".format(str(_err))

        return _error_code, _msg

    def calculate_criticality(self, item_hr):
        """
        Calculate the Criticality for the Mode.

            Mode Criticality = Item Hazard Rate * Mode Ratio *
                               Mode Operating Time * Effect Probability

        :param float item_hr: the hazard rate of the hardware item being
                              calculated.
        :return: (_error_code, _msg); the error code and associated message
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Calculating failure mode {0:d} criticality.'.\
            format(self.mode_id)

        if item_hr < 0.0:
            _error_code = 2010
            _msg = _("RAMSTK ERROR: Item hazard rate has a negative value.")
            raise OutOfRangeError(_msg)
        if not 0.0 <= self.mode_ratio <= 1.0:
            _error_code = 2010
            _msg = _(
                "RAMSTK ERROR: Failure mode ratio is outside the range of "
                "[0.0, 1.0].",
            )
            raise OutOfRangeError(_msg)
        if self.mode_op_time < 0.0:
            _error_code = 2010
            _msg = _("Failure mode operating time has a negative value.")
            raise OutOfRangeError(_msg)
        if not 0.0 <= self.effect_probability <= 1.0:
            _error_code = 2010
            _msg = _(
                "Failure effect probability is outside the range "
                "[0.0, 1.0].",
            )
            raise OutOfRangeError(_msg)

        self.mode_hazard_rate = item_hr * self.mode_ratio
        self.mode_criticality = self.mode_hazard_rate \
            * self.mode_op_time * self.effect_probability

        if self.mode_hazard_rate < 0.0:
            _error_code = 2010
            _msg = _("Failure mode hazard rate has a negative value.")
            raise OutOfRangeError(_msg)
        if self.mode_criticality < 0.0:
            _error_code = 2010
            _msg = _("Failure mode criticality has a negative value.")
            raise OutOfRangeError(_msg)

        return _error_code, _msg
